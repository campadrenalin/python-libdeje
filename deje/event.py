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

from deje.action import Action

class Event(Action):
    def __init__(self, content, author, version = None):
        self.deserialize({
            'type'    : 'event',
            'author'  : author,
            'content' : content,
            'version' : version,
        })

    def deserialize(self, items):
        Action.deserialize(self, items)
        self.content = self.overflow.pop('content')
        self.version = self.overflow.pop('version')

    @property
    def items(self):
        return {
            "type"    : self.atype,
            "author"  : self.author,
            "content" : self.content,
            "version" : self.version,
        }

    @property
    def quorum_threshold_type(self):
        return "write"

    def is_done(self, document):
        '''
        Returns whether Event has already been applied.
        '''
        return self in document._history.events

    def enact(self, quorum, document):
        '''
        Apply Event to the head of the document's history.
        '''
        document._history.add_event(self)
        document.signals['enact-event'].send(self)
        self.apply(document._current)

    def apply(self, state):
        '''
        Apply event to a given HistoryState.
        '''
        state.apply(self)

    def test(self, state):
        '''
        Return whether Event is valid for the given state.
        '''
        return state.interpreter.event_test(self.content, self.author)
