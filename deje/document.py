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

from __future__ import print_function
import dispatch

from deje import quorumspace
from deje.event import Event
from deje.read import ReadRequest
from deje.resource import Resource

def serialize_resources(resources):
    serialized = {}
    for resource in resources:
        path = resource.path
        serialized[path] = resource.serialize()
    return serialized

class Document(object):
    def __init__(self, name, handler_path="/handler.lua", resources=[], owner = None):
        self._name = name
        self._handler = handler_path
        self._owner = owner
        self._resources = {}
        self._originals = {}
        self._qs = quorumspace.QuorumSpace(self)
        self._blockchain = []
        self._interpreter = None
        self.signals = {
            'recv-version': dispatch.Signal(
                providing_args=['version']),
            'recv-block': dispatch.Signal(
                providing_args=['version','block']),
            'recv-snapshot':dispatch.Signal(
                providing_args=['version','snapshot']),
        }
        self.subscribers = set()
        for res in resources:
            self.add_resource(res, False)

    # High-level resource manipulation

    def add_resource(self, resource, interp_call = True):
        if interp_call:
            self.interpreter.on_resource_update(resource.path, 'add')
        self._resources[resource.path] = resource
        resource.document = self

    def get_resource(self, path):
        return self._resources[path]

    def del_resource(self, path, interp_call = True):
        if interp_call:
            self.interpreter.on_resource_update(path, 'delete')
        del self._resources[path]

    @property
    def resources(self):
        return self._resources

    @property
    def interpreter(self):
        if not self._interpreter:
            self._interpreter = self.handler.interpreter()
        return self._interpreter

    def snapshot(self, version = None):
        if version == None:
            version = self.version
        if version != self.version:
            raise NotImplementedError("Rewinds not supported yet")

        return serialize_resources(self.resources.values())

    def serialize(self):
        return {
            'original': serialize_resources(self._originals.values()),
            'events': self._blockchain
        }

    def deserialize(self, serial):
        self._resources = {}
        for resource in serial['original'].values():
            self.add_resource( Resource(source=resource), False )
        self.freeze()

        for event in serial['events']:
            ev = Event(event['content'], author = event['author'])
            self.external_event(ev)

    def freeze(self):
        '''
        Throw away history and base originals off of current state.
        '''
        self._originals = {}
        for path in self.resources:
            self._originals[path] = self.resources[path].clone()
        self._blockchain = []

    def eval(self, value):
        '''
        Evaluate code in handler context, returning result
        '''
        return self.interpreter.eval(value)

    def execute(self, value):
        '''
        Execute code in handler context
        '''
        return self.interpreter.execute(value)

    # Host requests

    def request(self, callback, *args):
        return self.interpreter.host_request(callback, args)

    # Event stuff

    def event(self, ev):
        '''
        Create a event from arbitrary object 'ev'
        '''
        if not self.can_write():
            raise ValueError("You don't have write permission")
        event = Event(self, ev, author = self.identity)
        return self.external_event(event)

    def external_event(self, event):
        if event.test():
            if self.owner:
                event.quorum.sign(self.identity)
                event.transmit()
            else:
                event.enact()
            return event
        else:
            raise ValueError("Event %r was not valid" % event.content)
        
    def subscribe(self):
        if not self.can_read():
            raise ValueError("You don't have read permission")
        request = ReadRequest(self)
        if self.owner:
            request.transmit()
        return request

    @property
    def competing(self):
        "All competing quorums"
        return self._qs.get_competing_actions()

    # Handler-derived properties

    def get_participants(self):
        return self.interpreter.quorum_participants()

    def get_thresholds(self):
        return self.interpreter.quorum_thresholds()

    def get_request_protocols(self):
        return self.interpreter.request_protocols()

    def can_read(self, ident = None):
        ident = ident or self.identity
        return self.interpreter.can_read(ident.key)

    def can_write(self, ident = None):
        ident = ident or self.identity
        return self.interpreter.can_write(ident.key)

    # Handler

    @property
    def handler(self):
        return self.get_resource(self._handler)

    def set_handler(self, path):
        self._handler = path

    # Other accessors

    @property
    def name(self):
        return self._name

    @property
    def owner(self):
        return self._owner

    @property
    def identity(self):
        if self.owner:
            return self.owner.identity
        else:
            raise AttributeError("Attempt to access identity of unowned doc")

    @property
    def version(self):
        return len(self._blockchain)

def load_from(filename):
    import json
    doc = Document(filename)
    serial = json.load(open(filename))
    doc.deserialize(serial)
    return doc

def save_to(doc, filename):
    import json
    json.dump(doc.serialize(), open(filename, 'w'))
