"""
Unit tests for ErrorParser.

Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import sys
sys.path.append("../../source")

from operations.ErrorParser import ErrorParser
from errors.SharedStackError import SharedStackError
from errors.Stack import Stack

valgrindLogFileName = "../valgrind.errors"
try:
  with open(valgrindLogFileName, "r") as valgrindLogFile:
    lines = valgrindLogFile.read().splitlines()
except:
  sys.exit("Could not read Valgrind log file '" + valgrindLogFileName + "'.")


if lines == None or len(lines) == 0:
  sys.exit("Did not get any lines from '" + valgrindLogFileName + "'.")

parser = ErrorParser()
errors, unknowns, id = parser.parse(lines)
errorTree = SharedStackError(errors, 0, Stack.FROM_BOTTOM)


if "--print" in sys.argv:
  errorTree.printTree()
