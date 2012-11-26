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

# Prebaked handlers for Lua interpreter

from deje import document, resource

def echo_chamber():
    '''
    Diagnostic, prints stuff on events.

    >>> doc = test_bootstrap(echo_chamber())

    >>> exampletxt = resource.Resource('/example.txt', 'blerg', type='text/plain')
    >>> doc.add_resource(exampletxt)
    on_resource_update /example.txt add
    >>> exampletxt.type = "marshmallow/cloud"
    on_resource_update /example.txt type
    >>> exampletxt.content = "I like turtles."
    on_resource_update /example.txt content
    >>> exampletxt.comment = "Meaningless drivel"
    on_resource_update /example.txt comment
    >>> exampletxt.path = "/fridge/turtles.txt"
    on_resource_update /fridge/turtles.txt path
    /example.txt was moved to /fridge/turtles.txt

    '''
    return '''
        function on_resource_update(path, propname, oldpath)
            deje.debug('on_resource_update ' .. path .. " " .. propname)
            if propname == 'path' then
                deje.debug(oldpath .. " was moved to " .. path)
            end
        end
    '''

def test_bootstrap(content):
    doc = document.Document()
    handler = resource.Resource('/handler.lua', content, 'The primary handler', 'text/lua')
    doc.add_resource(handler)
    return doc