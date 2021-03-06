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

import os
import tempfile

from ejtp.util.compat        import unittest
from ejtp.tests.test_scripts import IOMock

from deje.dexter.interface   import DexterInterface

class DexterDemoGroup(object):
    def __init__(self):
        self.log_obj = []

    def do_demo(self, args):
        self.log_obj.append(args)

class DexterCommandTester(unittest.TestCase):
    def setUp(self):
        self.io = IOMock()
        with self.io:
            self.interface = DexterInterface()
            self.commands  = self.interface.commands
            self.terminal  = self.interface.terminal

        self.demo_group = DexterDemoGroup()
        self.commands.groups.add(self.demo_group)

    def tearDown(self):
        self.terminal.stop()

    @property
    def demo_log(self):
        return self.demo_group.log_obj

class Tempfile(str):
    def __enter__(self):
        _, self.path = tempfile.mkstemp()
        return self.path

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.remove(self.path)
