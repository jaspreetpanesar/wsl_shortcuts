# -*- coding: utf-8 -*-

"""
Open explorer window in any location
"""

import os
from wsl_path import *

parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
parser.add_argument("command", nargs="?", type=str)
parser.add_argument("path", nargs="?", type=str)
args = parser.parse_args()

if args.command:
    try:
        path = convert_path(args.path)
        if path:
            os.system("%s %s" %(args.command, path))
    except Exception as e:
        print("Error: %s" %e)
else:
    print("Error: No command supplied")
