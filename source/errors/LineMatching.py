"""
Collection of utilities used for matching in, classifying of and data
extraction from text lines.

Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import re


class Patterns(object):
    """A collection of regular expressions that lines from the Valgrind log file can be matched against."""

    def __init__(self):
        """"""
        ## All lines printed by Valgrind begin with the ==<number>== marker.
        self.isValgrind = re.compile("^==\d+== .*$")
        self.stripValgrind = re.compile("^==\d+== (.*)")
        self.readId = re.compile("^==(\d+)== .*$")

        ## The following is a list of lines Valgrind prints that can safely be ignored.
        self.isHeader = re.compile(
          ".*Memcheck, a memory error detector" + "|" +
          ".*Copyright \(C\) \d+-\d+, and GNU GPL'd, by Julian Seward et al." + "|" +
          ".*Using Valgrind-\d+.\d+.\d+.* and LibVEX; rerun with -h for copyright info" + "|" +
          ".*Command: .*"
        )

        ## There are two types of stack frame lines; the top and the callers. They are
        ## different only in the first word.
        ##
        ## For example.
        ##  at 0x400A10: set() (errorProducingApplication.cpp:37)
        ##  by 0x400A68: work() (errorProducingApplication.cpp:44)
        ##
        ## The stack frame lines are constructed by Valgrind from various pieces of
        ## information and not all information is available in every line. The following
        ## is a listing of the pieces available. Named regular expression groups are
        ## used to allow for information inspection and extraction.

        # The address in memory of the instruction that gaused the error.
        address = "(?P<address>0x[a-fA-F0-9]+): "

        anonNamespace = "\(anonymous namespace\)"

        unknownMethod = "\(\?\)+?"
        properMethod = "(?P<method>(" + anonNamespace + ")?[\w:=+*~&? \[\]<>.,]+) ?"

        # The name of the method containing the instruction.
        method = "(?:(?:" + unknownMethod + ")|(?:" + properMethod + "))"

        # Argument list for the method.
        arguments = "(?P<arguments>(?:\([\w ,:*<>()&]*\))?) "

        # Any modifier, such as 'const', on the method.
        modifier = "(?P<modifier>[\w]*)? ?"

        # Source code location of the error.
        fileAndLine = "(?P<fileName>[\w /.+-]+.\w+):(?P<lineNumber>\d+)"

        # Compiled unit (e.g. .so file) that contains the offending instruction.
        library = "in (?P<library>[\w/.+-_]+)"

        ## Valgrind seems to always print either the source file with line number
        ## or the file name of the compiled binary.
        fileLib = "(?:(?:" + fileAndLine + ")|(?:" + library + "))"

        postMethod = "(?:" + arguments + modifier + ")?"

        ## The above components are combined into patterns for 'at' frames, 'by'
        ## frames or either.
        stackFrameShared = address + method + "(?:" + postMethod + "\(" + fileLib + "\)" + ")?"
        self.isStackFrameTop = re.compile(".*at " + stackFrameShared)
        self.isStackFrameCaller = re.compile(".*by " + stackFrameShared)
        self.isAnyStackFrame = re.compile(".*(?:(?:at)|(?:by)) " + stackFrameShared)

        ## Listing of Valgrind errors. This list may be incomplete. Errors not
        ## listed here will be ignored and hidden from the user.
        conditionalJumpOrMove = ".*Conditional jump or move depends on uninitialised value\(s\)$"
        self.isConditionalJumpOrMoveDependsOnUninitialisedValues = re.compile(conditionalJumpOrMove)
        self.isInvalidRead = re.compile(".*Invalid read of size \d+$")
        self.isInvalidWrite = re.compile(".*Invalid write of size \d+$")
        self.isMissmatchedFreeDelete = re.compile(".*Mismatched free\(\) / delete / delete \[\]")
        self.isInvalidFreeDelete = re.compile(".*Invalid free\(\) / delete / delete\[\] / realloc\(\)")

        directIndirec = "(?:\([\d,.]+ direct, [\d,.]+ indirect\))? ?"
        bytesBlocks = "bytes in [\d,.]+ blocks are "
        certainty = "(?:(?:possibly)|(?:definitely)) "
        record = "lost in loss record [\d,.]+ of [\d,.]+"
        isMemoryLoss = ".*[\d,.]+ " + directIndirec + bytesBlocks + certainty + record
        self.isMemoryLoss = re.compile(isMemoryLoss)

        ## Listing of Valgrind sources. A source is a separate call stack to some
        ## memory operation (allocate or deallocate) that has some relation to the
        ## detected error. Each such call stack in the Valgrind log has a header
        ## that matches the following pattern.
        memoryLocation = "(?:(?:before)|(?:inside)|(?:after))"
        memoryOperation = "(?:(?:alloc'd)|(?:free'd))"
        stackAllocation = "Uninitialised value was created by a heap allocation"
        self.isStackAllocation = re.compile(".*" + stackAllocation)

        address = "Address 0x[a-fA-F0-9]+ is "
        block = " a block of size \d+ "
        self.isHeapAllocation = re.compile(".*" + address + "\d+ bytes " + memoryLocation + block + memoryOperation)

    def isErrorStart(self, line):
        """Returns true if the given line matches a known Valgrind error."""

        return  self.isConditionalJumpOrMoveDependsOnUninitialisedValues.match(line) is not None or \
          self.isInvalidRead.match(line) is not None or \
          self.isInvalidWrite.match(line) is not None or \
          self.isMissmatchedFreeDelete.match(line) is not None or \
          self.isInvalidFreeDelete.match(line) is not None or \
          self.isMemoryLoss.match(line) is not None

    def isSourceStart(self, line):
        """Returns true if the given line matches a known error source."""

        return self.isStackAllocation.match(line) is not None or \
            self.isHeapAllocation.match(line) is not None
