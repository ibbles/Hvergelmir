"""
Tests for the regular expression patterns found in LineMatching.py.

Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""



import sys
sys.path.append("../../source")

from errors.LineMatching import Patterns

patterns = Patterns();

logFileName = "../valgrind.errors"
try :
  with open(logFileName) as logFile:
    lines = logFile.read().splitlines()
except:
  sys.exit("Could not read file '" + logFileName + "'.")


## These numbers have been found by running the test and recording the number
## of matches found. The tester therefore passed at that time by definition.
## The numbers may be wrong, It this test fails then we need to manually, or
## by using some external tool, count the actual number of expected matches
## for each pattern. When doing this, mark the numbers that has been verified.
## When all lines has been verified then this comment and the marks can be
## removed.
expectedTotal = 367 # Verified.
expectedValgrind = 347 # Verified.
expectedHeader = 4 # Verified
expectStackTop = 56
expectStackCaller = 187
expectAnyStack = 243
expectDependUnitialized = 14
expectInvalidRead = 7
expectInvalidWrite = 4
expectMissmatchFreeDelete = 2
expectInvalidFreeDelete = 0
expectMemoryLoss = 0
expectStackAllocation = 14
expectHeapAllocation = 13
expectError = 27
expectSource = 27

numValgrind = 0;
numHeader = 0
numStackTop = 0
numStackCaller = 0
numAnyStack = 0
numDependUninitialized = 0
numInvalidRead = 0
numInvalidWrite = 0
numMissmatchFreeDelete = 0
numInvalidFreeDelete = 0
numMemoryLoss = 0
numStackAllocation = 0
numHeapAllocation = 0
numError = 0
numSource = 0

for line in lines:
  if patterns.isValgrind.match(line) != None:
    numValgrind += 1
  if patterns.isHeader.match(line) != None:
    numHeader += 1
  if patterns.isStackFrameTop.match(line) != None:
    numStackTop += 1
  if patterns.isStackFrameCaller.match(line) != None:
    numStackCaller += 1
  if patterns.isAnyStackFrame.match(line) != None:
    numAnyStack += 1
  if patterns.isConditionalJumpOrMoveDependsOnUninitialisedValues.match(line) != None:
    numDependUninitialized += 1
  if patterns.isInvalidRead.match(line) != None:
    numInvalidRead += 1
  if patterns.isInvalidWrite.match(line) != None:
    numInvalidWrite += 1
  if patterns.isMissmatchedFreeDelete.match(line) != None:
    numMissmatchFreeDelete += 1
  if patterns.isInvalidFreeDelete.match(line) != None:
    numInvalidFreeDelete += 1
  if patterns.isMemoryLoss.match(line) != None:
    numMemoryLoss += 1
  if patterns.isStackAllocation.match(line) != None:
    numStackAllocation += 1
  if patterns.isHeapAllocation.match(line) != None:
    numHeapAllocation += 1
  if patterns.isErrorStart(line):
    numError += 1
  if patterns.isSourceStart(line):
    numSource += 1

if len(sys.argv) > 1 and sys.argv[1] == "--verbose":
  print(str(len(lines)) + " lines in total.")
  print(str(numValgrind) + " lines are valgrind lines.")
  print(str(numHeader) + " lines are header lines.")
  print(str(numStackTop) + " lines are stack tops.")
  print(str(numStackCaller) + " lines are stack callers.")
  print(str(numAnyStack) + " lines are any stack frame.")
  print(str(numDependUninitialized) + " lines are jump or move using uninitialized.")
  print(str(numInvalidRead) + " lines are invalid reads.")
  print(str(numInvalidWrite) + " lines are invalid writes.")
  print(str(numMissmatchFreeDelete) + " lines are missmatched free/delte.")
  print(str(numInvalidFreeDelete) + " lines are invalid free/delete.")
  print(str(numMemoryLoss) + " lines are memory loss.")
  print(str(numStackAllocation) + " lines are stack allocation source lines.")
  print(str(numHeapAllocation) + " lines are heap allocation source lines.")
  print(str(numError) + " lines are error start.")
  print(str(numSource) + " lines are source.")

assert len(lines) == expectedTotal, "Did not get the expected number of lines from the test log file. Has the log been changed?"
assert numValgrind == expectedValgrind, "Did not find the expected number of Valgrind lines."
assert numHeader == expectedHeader, "Did not find the expected number of header lines."
assert numStackTop == expectStackTop, "Did not find the expected number of stack tops."
assert numStackCaller == expectStackCaller, "Did not find the expected number of stack callers. Expected " + str(expectStackCaller) + " but found " + str(numStackCaller) +"."
assert numAnyStack == expectAnyStack, "Did not find the expected number of stack frames. Expected " + str(expectAnyStack) + " but found " + str(numAnyStack) +"."
assert numAnyStack == numStackTop + numStackCaller, "Stack tops and stack callers does not add up sum of stack frames."
assert numDependUninitialized == expectDependUnitialized, "Did not find the expected number of uninitialized jump."
assert numInvalidRead == expectInvalidRead, "Did not find the expected number of invalid reads."
assert numInvalidWrite == expectInvalidWrite, "Did not find the expected number of invalid writes."
assert numMissmatchFreeDelete == expectMissmatchFreeDelete, "Did not find the expected number of missmatched free/delete."
assert numInvalidFreeDelete == expectInvalidFreeDelete, "Did not find the expected number of invalid free/delete."
assert numMemoryLoss == expectMemoryLoss, "Did not find the expected number of memory loss."
assert numStackAllocation == expectStackAllocation, "Did not find the expected number of stack allocation sources."
assert numHeapAllocation == expectHeapAllocation, "Did not find the expected number of head allocation sources."
assert numError == expectError, "Did not find the expected number of error starts."
assert numSource == expectSource, "Did not find the expected number of sources."