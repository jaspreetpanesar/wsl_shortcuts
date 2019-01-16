# -*- coding: utf-8 -*-

"""
Open explorer window in any location
"""

import os
from path import *

class NoCommandSuppliedException(Exception):
    pass


def runCommand(command, path):
    """
    runs provided command in shell and supplies absoloute path
    to command
    
    Args:
        arg1 (type): explanation
        command (string): the command to run - if command is space seperated
            add quites around string
        path (string): the relative path to be converted to absoloute
            path - if path is empty, local directory is used
    
    Raises:
        NoCommandSuppliedException: if no command was supplied
    """
    if command:
        newpath = convert_path(path)
        if newpath:
            os.system("%s %s" %(command, newpath))
    else:
        raise NoCommandSuppliedException("No command supplied")


def main(args):
    try:
        runCommand(args.command, args.path)
    except (NoCommandSuppliedException, PathDoesNotExistException) as e:
        print("Error: %s" %e)


if __name__ == "__main__":
    # read command and path from 
    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
    parser.add_argument("command", nargs="?", type=str)
    parser.add_argument("path", nargs="?", type=str)
    args = parser.parse_args()
    main(args)


