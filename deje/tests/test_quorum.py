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

from __future__ import absolute_import

from deje.tests.stream   import StreamTest

from deje.event          import Event
from deje.quorum         import Quorum
from deje.handlers       import handler_document
from deje.tests.identity import identity
from deje.owner          import Owner

class TestQuorum(StreamTest):

    def setUp(self):
        StreamTest.setUp(self)

        self.doc = handler_document("echo_chamber")
        self.ev  = Event({'x':'y'}, identity("atlas"), self.doc.version)
        self.quorum = Quorum(self.ev, self.doc._qs)
        self.quorum.document = self.doc
        self.ident = identity()
        self.owner = Owner(self.ident, make_jack=False)
        self.owner.own_document(self.doc)
        self.owner.identities.update_ident(self.ev.author)

    def test_clear(self):
        self.quorum.sign(self.ident)
        self.assertEqual(self.quorum.completion, 1)

        self.quorum.clear()
        self.assertEqual(self.quorum.completion, 0)

    def test_completion(self):
        self.assertEqual(self.quorum.completion, 0)
        self.quorum.sign(self.ident)
        self.assertEqual(self.quorum.completion, 1)

    def test_outdated(self):
        self.assertEqual(self.doc.version, 'current')
        self.assertEqual(self.doc._qs.version, 'current')
        self.assertEqual(self.ev.version, 'current')
        self.assertEqual(self.quorum.version, 'current')
        self.assertFalse(self.quorum.outdated)

        self.quorum.sign(self.ident)
        self.assertFalse(self.quorum.outdated)

        self.owner.protocol.paxos.check_quorum(self.doc, self.ev)
        # Stupid Python 2 makes this the easiest way to put up with string crap
        output = self.getOutput()
        self.assertIn(output, [
            "Event '{'x': 'y'}' achieved.\n",
            "Event '{u'x': u'y'}' achieved.\n",
        ])

        self.assertEqual(self.doc.version, self.ev.hash())
        self.assertEqual(self.quorum.version, 'current')
        self.assertTrue(self.quorum.outdated)

    def test_participants(self):
        self.assertEqual(self.quorum.participants, [self.ident])

    def test_thresholds(self):
        self.assertEqual(self.quorum.thresholds, {'read':1, 'write':1})

    def test_threshold(self):
        self.assertEqual(self.quorum.threshold, 1)
