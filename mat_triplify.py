#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dfs

Usage:
  dfs  FILE
  dfs -h | --help
  dfs --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from __future__ import unicode_literals, print_function
from docopt import docopt
import csv

__version__ = "0.1.0"
__author__ = "Charles Vardeman"
__license__ = "MIT"




def main():
    """Main entry point for the dfs CLI."""
    args = docopt(__doc__, version=__version__)
    csvfile = args["FILE"]
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row[1])


if __name__ == '__main__':
    main()
