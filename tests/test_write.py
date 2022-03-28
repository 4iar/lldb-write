import unittest
import subprocess
import tempfile
from pathlib import Path


class TestWrite(unittest.TestCase):

    def setUp(self) -> None:
        self.working_dir_handle = tempfile.TemporaryDirectory()
        self.working_dir_path = Path(self.working_dir_handle.name)
        self.binary_path = self.working_dir_path / 'helloworld'

        program_str = '''
        #include <stdio.h>
        
        int main () {
            printf("Hello, world! :)");
            return 0;
        }
        '''

        program_source_path = self.working_dir_path / 'helloworld.c'
        with open(program_source_path, 'w') as f:
            f.write(program_str)

        subprocess.run(['gcc', program_source_path, '-o', self.binary_path], check=True)

    def tearDown(self):
        self.working_dir_handle.cleanup()

    def test_loads_correctly(self):
        stdout = subprocess.run(['lldb', self.binary_path, '--batch', '-o', 'command script import write.py'],
                                 check=True,
                                 capture_output=True).stdout.decode('utf-8')

        self.assertIn('The "write" command has been loaded and is ready for use.', stdout)

    def test_writes_to_file(self):
        output_file = self.working_dir_path / 'breakpoint.txt'
        subprocess.run(['lldb', self.binary_path, '--batch', '-o', 'command script import write.py', '-o', f'write {output_file} b'],
                                 check=True)

        expected_contents = '''(lldb) b\n\nNo breakpoints currently set.\n'''

        with open(output_file, 'r') as f:
            actual_contents = f.read()

        self.assertEqual(actual_contents, expected_contents)
















































