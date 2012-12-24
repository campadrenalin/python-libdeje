'''
This file is part of python-libdeje.

python-libdeje is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-libdeje is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with python-libdeje.  If not, see <http://www.gnu.org/licenses/>.
'''

import ejtp.client
import identity
import checkpoint
import read
import document

class Owner(object):
    '''
    Manages documents, identities, and an EJTP client.
    '''
    def __init__(self, self_ident, router=None, make_jack=True):
        '''
        Make sure string idents fail
        >>> from ejtp.router import Router
        >>> anon = Owner("anonymous", Router())
        Traceback (most recent call last):
        AttributeError: 'str' object has no attribute 'location'

        Make sure self_idents with no location fail
        >>> import testing
        >>> badident = testing.identity()
        >>> badident.location = None
        >>> Owner(badident, None, False)
        Traceback (most recent call last):
        AttributeError: Identity location not set

        Do setup for testing a good owner.
        >>> owner = testing.owner()
        >>> owner.identities #doctest: +ELLIPSIS
        <EncryptorCache '{\\'["local",null,"mitzi"]\\': <deje.identity.Identity object at ...>}'>
        >>> doc = testing.document(handler_lua_template="echo_chamber")
        >>> doc.handler #doctest: +ELLIPSIS
        <deje.resource.Resource object at ...>
        >>> owner.own_document(doc)

        '''
        self.identities = identity.EncryptorCache()
        self.identities.update_ident(self_ident)
        self.identity = self_ident

        self.documents  = {}
        self.client = ejtp.client.Client(router, self.identity.location, self.identities, make_jack)
        self.client.rcv_callback = self.on_ejtp

    def own_document(self, document):
        document._owner = self
        self.documents[document.name] = document

    # EJTP callbacks

    def on_ejtp(self, msg, client):
        '''
        >>> import testing
        >>> mitzi, atlas, victor, mdoc, adoc, vdoc = testing.ejtp_test()

        >>> mitzi.identity.location
        ['local', None, 'mitzi']
        >>> atlas.identity.location
        ['local', None, 'atlas']
        >>> mitzi.client.interface == mitzi.identity.location
        True
        >>> r = mitzi.client.router
        >>> r.client(mitzi.identity.location) == mitzi.client
        True
        >>> atlas.client.interface == atlas.identity.location
        True
        >>> mitzi.client.router == atlas.client.router
        True

        Test raw EJTP connectivity with a malformed message
        >>> atlas.client.write_json(mitzi.identity.location, "Oompa loompa")
        Recieved non-{} message, dropping
        '''
        content = msg.jsoncontent
        # Rule out basic errors
        if type(content) != dict:
            print "Recieved non-{} message, dropping"
            return
        if not "type" in content:
            print "Recieved message with no type, dropping"
            return

        # Accumulate basic information
        mtype = content['type']
        if "docname" in content and content['docname'] in self.documents:
            doc = self.documents[content['docname']]
        else:
            doc = None

        # Find and call function
        funcname = "_on_" + mtype.replace('-','_')
        if hasattr(self, funcname):
            func = getattr(self, funcname)
            func(msg, content, mtype, doc)
        else:
            print "Recieved message with unknown type (%r)" % mtype

    def _on_deje_lock_acquire(self, msg, content, ctype, doc):
        lcontent = content['content']
        ltype = lcontent['type']
        if ltype == "deje-checkpoint":
            cp_content = lcontent['checkpoint']
            cp_version = lcontent['version']
            cp_author  = lcontent['author']

            cp = checkpoint.Checkpoint(doc, cp_content, cp_version, cp_author)
            if doc.can_write(cp_author) and cp.test():
                cp.quorum.sign(self.identity)
                cp.quorum.transmit([self.identity.name])
        if ltype == "deje-subscribe":
            rr_subname = lcontent['subscriber']
            subscriber = self.identities.find_by_name(rr_subname)
            rr = read.ReadRequest(doc, subscriber)
            if doc.can_read(subscriber):
                rr.sign(self.identity)
                rr.update()

    def _on_deje_lock_acquired(self, msg, content, ctype, doc):
        sender = self.identities.find_by_name(content['signer'])
        try:
            cp = doc._qs.by_hash[content['content-hash']].parent
        except KeyError:
            print "Unknown checkpoint data, dropping"
            return
        sig = content['signature'].encode('raw_unicode_escape')
        cp.quorum.sign(sender, sig)
        cp.update()

    def _on_deje_lock_complete(self, msg, content, ctype, doc):
        try:
            quorum = doc._qs.by_hash[content['content-hash']]
        except KeyError:
            print "Unknown checkpoint data for complete, dropping (%r)" % content['content-hash']
            return
        for signer in content['signatures']:
            sender = self.identities.find_by_name(signer)
            sig = content['signatures'][signer].encode('raw_unicode_escape')
            quorum.sign(sender, sig)
            quorum.parent.update()

    def _on_deje_get_version(self, msg, content, ctype, doc):
        sender = self.identities.find_by_location(msg.addr)
        if not doc.can_read(sender):
            print "Permissions error: cannot read"
            return
        self.reply(doc, 'deje-doc-version', {'version':doc.version}, sender)

    def _on_deje_doc_version(self, msg, content, ctype, doc):
        sender = self.identities.find_by_location(msg.addr)
        if sender.name not in doc.get_participants():
            print "Version information came from non-participant source, ignoring"
            return
        version = content['version']
        doc.trigger_callback('recv-version', version)

    def _on_deje_get_block(self, msg, content, ctype, doc):
        sender = self.identities.find_by_location(msg.addr)
        blocknumber = content['version']
        blockcp = doc._blockchain[blocknumber]
        block = {
            'author': blockcp.authorname,
            'content': blockcp.content,
            'version': blockcp.version,
            'signatures': blockcp.quorum.sigs_dict(),
        }
        if not doc.can_read(sender):
            print "Permissions error: cannot read"
            return
        self.reply(doc, 'deje-doc-block', {'block':block}, sender)

    def _on_deje_doc_block(self, msg, content, ctype, doc):
        sender = self.identities.find_by_location(msg.addr)
        if sender.name not in doc.get_participants():
            print "Block information came from non-participant source, ignoring"
            return
        block = content['block']
        version = block['version']
        doc.trigger_callback('recv-block-%d' % version, block)


    # Network utility functions

    def transmit(self, document, mtype, properties, targets = [], participants = False, subscribers = True):
        targets = set(targets)
        if participants:
            targets.update(set(document.get_participants()))
        if subscribers:
            targets.update(document.subscribers)

        message = { 'type':mtype, 'docname':document.name }
        message.update(properties)
        for target in targets:
            # print target, mtype
            if hasattr(target, 'location'):
                address = target.location
            else:
                try:
                    address = self.identities.find_by_name(target).location
                except KeyError:
                    print "No known address for %r, skipping" % target
                    break
            if address != self.identity.location:
                self.client.write_json(address, message)

    def reply(self, document, mtype, properties, target):
        return self.transmit(document, mtype, properties, [target], subscribers=False)

    def lock_action(self, document, content, actiontype = None):
        self.transmit(document, 'deje-lock-acquire', {'content':content}, participants = True, subscribers=False)

    # Network actions

    def get_version(self, document, callback):
        """
        >>> import testing
        >>> mitzi, atlas, victor, mdoc, adoc, vdoc = testing.ejtp_test()
        >>> def on_recv_version(version):
        ...     print "Version is %d" % version
        >>> victor.get_version(vdoc, on_recv_version)
        Version is 0
        >>> mcp = mdoc.checkpoint({ #doctest: +ELLIPSIS
        ...     'path':'/example',
        ...     'property':'content',
        ...     'value':'Mitzi says hi',
        ... })
        >>> victor.get_version(vdoc, on_recv_version)
        Version is 1
        """
        document.set_callback('recv-version', callback)
        self.transmit(document, 'deje-get-version', {}, participants = True, subscribers = False)

    def get_block(self, document, version, callback):
        """
        >>> import json
        >>> import testing
        >>> mitzi, atlas, victor, mdoc, adoc, vdoc = testing.ejtp_test()

        Print in a predictible manner for doctest

        >>> def on_recv_block(block):
        ...     keys = block.keys()
        ...     keys.sort()
        ...     for key in keys:
        ...         print key + ": " + json.dumps(block[key], indent=4)

        Put in a checkpoint to retrieve

        >>> mcp = mdoc.checkpoint({ #doctest: +ELLIPSIS
        ...     'path':'/example',
        ...     'property':'content',
        ...     'value':'Mitzi says hi',
        ... })

        Retrieve checkpoint

        >>> victor.get_block(vdoc, 0, on_recv_block) #doctest: +ELLIPSIS
        author: "mitzi@lackadaisy.com"
        content: {
            "path": "/example", 
            "property": "content", 
            "value": "Mitzi says hi"
        }
        signatures: {
            "atlas@lackadaisy.com": "...", 
            "mitzi@lackadaisy.com": "..."
        }
        version: 0
        """
        document.set_callback('recv-block-%d' % version, callback)
        self.transmit(document, 'deje-get-block', {'version':version}, participants = True, subscribers = False)

    def get_snapshot(self, document, callback):
        document.set_callback('recv-snapshot-%d' % version, callback)
        self.transmit(document, 'deje-get-snapshot', {}, participants = True, subscribers = False)

    def error(self, recipients, code, explanation="", data={}):
        for r in recipients:
            self.client.write_json(r, {
                'type':'deje-error',
                'code':int(code),
                'explanation':str(explanation),
                'data':data,
            })
