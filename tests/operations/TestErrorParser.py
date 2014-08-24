"""
Unit tests for ErrorParser.

Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import sys
sys.path.append("../../source")

from operations.ErrorParser import ErrorParser


valgrindLogFileName = "../valgrind.errors"
try:
  with open(valgrindLogFileName, "r") as valgrindLogFile:
    lines = valgrindLogFile.read().splitlines()
except:
  sys.exit("Could not read Valgrind log file '" + valgrindLogFileName + "'.")


if lines == None or len(lines) == 0:
  sys.exit("Did not get any lines from '" + valgrindLogFileName + "'.")

parser = ErrorParser()
errors, unknowns = parser.parse(lines)

assert errors != None, "Get None error list from parser."
assert unknowns != None, "Got None unknowns list from parser."



if len(sys.argv) > 1 and sys.argv[1] == "--verbose":
  print("Got " + str(len(errors)) + " errors and " + str(len(unknowns)) + " unknowns.")
  
  print("Errors:")
  for error in errors:
    print(str(error))
  
  print("unknowns:")
  for unknown in unknowns:
    print("<"+str(unknown)+">")


assert len(errors) == 27, "Did not get the expected number of errors."
assert (len(unknowns)) == 19, "Did not get the expected number of unknowns."

