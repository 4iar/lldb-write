import argparse
import sys


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


def handle_call(debugger, raw_args, result, internal_dict):
    """Receives and handles the call to write from lldb"""
    args = parse_args(raw_args)

    f = open('./' + args.filename, 'w')
    debugger.SetOutputFileHandle(output, True);

    debugger.HandleCommand(args.command)

    debugger.SetOutputFileHandle(sys.stdout, True)

    f.close()


def __lldb_init_module(debugger, internal_dict):
    """Initialise the write command within lldb"""
    # Tell lldb to import this script and alias it as 'write'.
    # > Note: 'write' (from 'write.handle_call') is taken from the
    #   name of this file
    debugger.HandleCommand('command script add -f write.handle_call write')

    print('The "write" command has been loaded and is ready for use.')

