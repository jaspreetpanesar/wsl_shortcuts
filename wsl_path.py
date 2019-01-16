# -*- coding: utf-8 -*-

"""
**Formatted Path**

Returns the absoloute windows filesystem path of a directory
or file to be used in WSL.
"""

import logging
import argparse
import os
import sys

# ----- LOGGING SETUP -----
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# error logging
try:
    fh = logging.FileHandler("logs/wsl_path.log")
    fh.setLevel(logging.ERROR)
    fh.setFormatter(formatter)
    log.addHandler(fh)
except IOError:
    nh = logging.NullHandler()
    log.addHandler(nh)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(logging.Formatter("%(message)s"))
log.addHandler(ch)
# --- END LOGGING SETUP ---


# read wsl path from environment variables
try:
    WSL_ROOT = os.environ["WSL_ROOT"].split("/")
    WSL_DRIVE = os.environ["WSL_DRIVE"]
except (KeyError, Exception) as e:
    raise ImportError("Environment variables could not be found: %s" %e)


class PathDoesNotExistException(Exception):
    pass



class Path(object):

    def __init__(self, path):
        
        if not os.path.isdir(path) and not os.path.isfile(path):
            raise PathDoesNotExistException("Location does not exist")

        self.drive = "?"

        # convert relative paths to absoloute path
        # remove index 0, which is empty
        self.path = os.path.abspath(path).split("/")[1:]
        self.convert()


    def isWindows(self):
        """
        is path a location in the windows filesystem?

        Returns:
            bool: True if in windows filesystem, False if not
        """
        return self.path[0] == "mnt"


    def convert(self):
        """
        convert linux path style to windows path style

        Returns:
            string: absoloute windows filesystem path
        """
        if self.isWindows():
            # remove 'mnt', extract drive letter, remove drive letter
            del self.path[0]
            self.drive = self.path[0].upper()
            del self.path[0]
        else:
            # prepend wsl root windows path and drive from
            # user configured location
            for i in WSL_ROOT[::-1]:
                self.path.insert(0, i)
            self.drive = WSL_DRIVE


    def toString(self):
        string = "%s:\\" %self.drive.upper()
        for i in self.path:
            string += "%s\\" %i
        string = string.rstrip("\\")
        return string


    def __repr__(self):
        return "<%s(\"%s\")>" %(type(self).__name__, self.toString())




def convert_path(path):
    """
    Args:
        path (string): directory or file location
    
    Returns:
        string: windows formatted absolute path
    """
    if path:
        rpath = Path(path)
    else:
        rpath = Path(os.environ["PWD"])
    return "'%s'" %rpath.toString()


def main(path):
    try:
        print(convert_path(path))
    except PathDoesNotExistException as e:
        log.error("Error: %s (%s)" %(e, path))


if __name__ == "__main__":
    
    # setup argument parser to read path from user
    parser = argparse.ArgumentParser(
                prog="python wsl_path.py [path]",
                description=__doc__
                )
    parser.add_argument("path", nargs="?", type=str, 
            help="file/directory path or empty for current directory")
    args = parser.parse_args()

    main(args.path)



