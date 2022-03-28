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

    def test_handles_commands_with_arguments(self):
        output_file = self.working_dir_path / 'arguments.txt'
        subprocess.run(['lldb', self.binary_path, '--batch', '-o', 'command script import write.py', '-o',
                        f'write {output_file} platform shell echo --this-is-an-argument'],
                       check=True)

        expected_contents = '''(lldb) platform shell echo --this-is-an-argument\n\n--this-is-an-argument\n'''

        with open(output_file, 'r') as f:
            actual_contents = f.read()

        self.assertEqual(actual_contents, expected_contents)

    def test_shows_error_message_for_no_arguments(self):
        stderr = subprocess.run(['lldb', self.binary_path, '--batch', '-o', 'command script import write.py', '-o',
                       'write'],
                       check=True,
                       capture_output=True).stderr.decode('utf-8')

        expected_error_message = "too few arguments"
        self.assertIn(expected_error_message, stderr)

    def test_shows_error_message_for_one_argument(self):
        output_file = self.working_dir_path / 'parsing.txt'
        stderr = subprocess.run(['lldb', self.binary_path, '--batch', '-o', 'command script import write.py', '-o',
                       f'write {output_file}'],
                       check=True,
                       capture_output=True).stderr.decode('utf-8')

        expected_error_message = "too few arguments"
        self.assertIn(expected_error_message, stderr)
        self.assertFalse(output_file.exists())  # Nothing should be written to the file if the script wasn't called correctly!












































