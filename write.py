from __future__ import print_function
import lldb
import argparse
import re


def parse_args(raw_args):
    """Parse the arguments given to write"""
    args = raw_args.split(' ')

    if len(args) < 2:
        raise ValueError('write: too few arguments\nusage: write filename command [command ...]')

    filename = args[0]
    command = ' '.join(args[1:])

    return filename, command


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
    filename, command = parse_args(raw_args)

    # Run the command and store the result
    res = lldb.SBCommandReturnObject()
    interpreter = lldb.debugger.GetCommandInterpreter()
    interpreter.HandleCommand(command, res)

    # Get the output even
    output = res.GetOutput() or res.GetError()
    print(output, end='')
    write_to_file(filename, command, output)


def __lldb_init_module(debugger, internal_dict):
    """Initialise the write command within lldb"""
    # Tell lldb to import this script and alias it as 'write'.
    # > Note: 'write' (from 'write.handle_call') is taken from the
    #   name of this file
    debugger.HandleCommand('command script add -f write.handle_call write')

    print('The "write" command has been loaded and is ready for use.')
