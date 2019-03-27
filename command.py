# -*- coding: utf-8 -*-

"""
Run command in shell with absolute windows path
"""

import os
from path import *

class NoCommandSuppliedException(Exception):
    pass


def runCommand(command, paths):
    """
    runs provided command in shell and supplies absolute path
    to command
    
    Args:
        command (string): the command to run - if command is space seperated
            add quites around string
        paths [string, string, ..]: the relative paths to be converted to absolute
            paths - if path is empty, local directory is used
    
    Raises:
        NoCommandSuppliedException: if no command was supplied
    """
    if command:
        command_str = "%s " %command
        if len(paths) > 0:
            for path in paths:
                command_str += "%s " %convert_path(path)
        else:
            # use empty for current directory if no path provided
            command_str += convert_path('') 
        os.system(command_str.rstrip()) # remove trailing whitespace from adding paths
    else:
        raise NoCommandSuppliedException("No command supplied")


def main(args):
    try:
        runCommand(args.command, args.path)
    except (NoCommandSuppliedException, PathDoesNotExistException) as e:
        print("Error: %s" %e)


if __name__ == "__main__":
    # read command and path from arguments
    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
    parser.add_argument("command", nargs="?", type=str)
    parser.add_argument("path", nargs="*", type=str)
    args = parser.parse_args()
    main(args)


