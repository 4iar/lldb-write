from __future__ import print_function
import lldb
import argparse
import re


def parse_args(raw_args):
    """Parse the arguments given to write"""
    # Need to provide 'prog' (name of program) here otherwise
    # argparse tries to get it from sys.argv[0], which breaks
    # when called in lldb.
    parser = argparse.ArgumentParser(
        prog='write',
        description='Write the output of an lldb command to file'
    )

    parser.add_argument('filename')
    parser.add_argument('command', nargs='+')

    args = parser.parse_args(raw_args.split(' '))

    # The parser splits the command into a list of strings e.g.
    # ['register', 'read']
    # we convert it back to a string so we can later pass it to
    # lldb for evaluation
    args.command = ' '.join(args.command)

    return args


def strip_esc_seq(s):
    """Strip ANSI escape sequences from string."""
    esc_seq_re = re.compile(r'\x1b[^m]*m')
    return esc_seq_re.sub('', s)


def write_to_file(filename, command, output):
    """Write the output to the given file, headed by the command"""
    with open(filename, 'w') as f:
        f.write("(lldb) " + command + '\n\n')
        f.write(strip_esc_seq(output))


def handle_call(debugger, raw_args, result, internal_dict):
    """Receives and handles the call to write from lldb"""
    args = parse_args(raw_args)

    # Run the command and store the result
    res = lldb.SBCommandReturnObject()
    interpreter = lldb.debugger.GetCommandInterpreter()
    interpreter.HandleCommand(args.command, res)

    # Get the output even
    output = res.GetOutput() or res.GetError()
    print(output, end='')
    write_to_file(args.filename, args.command, output)


def __lldb_init_module(debugger, internal_dict):
    """Initialise the write command within lldb"""
    # Tell lldb to import this script and alias it as 'write'.
    # > Note: 'write' (from 'write.handle_call') is taken from the
    #   name of this file
    debugger.HandleCommand('command script add -f write.handle_call write')

    print('The "write" command has been loaded and is ready for use.')

