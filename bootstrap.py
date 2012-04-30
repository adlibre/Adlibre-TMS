#!/usr/bin/env python

# AC: 2012-04-30 This file and pip-reqs are deprecated. Use setup.py instead.

# Bootstrap and setup a virtualenv with the specified requirements.txt

import os
import sys
import subprocess
from optparse import OptionParser


usage = """usage: %prog [options]"""
parser = OptionParser(usage=usage)
parser.add_option("-c", "--clear", dest="clear", action="store_true",
                  help="clear out existing virtualenv")


def main():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found.\n\n")
        parser.print_usage()
        sys.exit(-1)
    (options, pos_args) = parser.parse_args()
    virtualenv = os.environ["VIRTUAL_ENV"]
    if options.clear:
        subprocess.call(["virtualenv", "--clear", "--no-site-packages", virtualenv])
    file_path = os.path.dirname(__file__)
    subprocess.call(["pip", "install", "-E", virtualenv, "--requirement",
                     os.path.join(file_path, "deployment/pip-req.txt")])


if __name__ == "__main__":
    main()
    sys.exit(0)
