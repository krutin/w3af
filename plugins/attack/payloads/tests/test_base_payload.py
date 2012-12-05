'''
test_Payload.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import unittest

from plugins.attack.payloads.base_payload import Payload
from core.data.kb.shell import shell


class TestBasePayload(unittest.TestCase):
    
    def setUp(self):
        self.bp = Payload(None)
    
    def test_can_run(self):
        self.assertEqual(self.bp.can_run(), set())
    
    def test_run_only_read(self):
        bp = Payload(None)
        self.assertRaises(AttributeError, bp.run, 'filename')

    def test_run_execute(self):
        class Executable(Payload):
            called_run_execute = False
            called_api_execute = False
            
            def run_execute(self, cmd):
                self.called_run_execute = True
                self.shell.execute(cmd)

            def api_execute(self, cmd):
                self.called_api_execute = True
        
        class FakeShell(shell):
            called_execute = False
            
            def __init__(self): pass
            
            def execute(self, cmd):
                self.called_execute = True
                
        executable = Executable(FakeShell())
        
        self.assertEqual(self.bp.can_run(), set())
        
        executable.run('command')
        self.assertTrue(executable.called_run_execute)
        self.assertTrue(executable.shell.called_execute)

        executable.run_api('command')
        self.assertTrue(executable.called_api_execute)
        