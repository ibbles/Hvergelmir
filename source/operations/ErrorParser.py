"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

from errors.LineMatching import Patterns
from errors.ParsedError import ParsedError

class ErrorParser(object):
  """Converts a list of strings, the Valgrind log, to a list of ParsedErrors."""

  def __init__(self):
    self.patterns = Patterns()
    self.resetState()



  def parse(self, lines): # (ParsedError list, string list, process id)
    """Parser ParsedErrors from the given line list. All elements of 'lines'
    must be string-like. None elements are not allowed.
    @param lines - String list - The contents of a Valgrind log.
    @return (ParsedError list, string list, process id) tuple containing the
            errors found and a list of unknown valgrind lines, or None if there
            was an error before any errors could be read. Process id is the PID
            extracted from the Valgrind log file.
    """

    setupSuccessful = self.setupState(lines)
    if not setupSuccessful:
      return (None, None, None)

    self.parseImplementation()

    id = self.id
    errorList = self.errors
    unknownErrors = self.unknownErrors
    self.resetState()
    return  (errorList, unknownErrors, id)



  def resetState(self): # None
    """Prepare the parser for a new round of parsing. The parser is placed in a
    dormant state, waiting for the next call to parse().
    """

    self.lines = None
    self.line = None
    self.currentLine = None



  def setupState(self, lines): # Boolean
    """Prepare the parser for parsing from the given string list."""

    if lines == None or len(lines) == 0:
      return False

    self.errors = [] # ParsedError list.
    self.unknownErrors = [] # String list. Lines that the parser didn't recognize.

    self.id = None
    self.lines = lines # String list. Provided by user.
    self.currentLine = 0 # Integer. The index of 'line' in 'lines'.
    self.line = self.lines[self.currentLine] # String. One of the string in 'lines'. Is always either None or a Valgrind line.
    return self.initFirstLine()



  def isParsing(self): # Boolean
    """Returns True if the parser is valid for continued parsing. Calling
    resetState will cause future calls to isParsing to return False until
    setupState is called.
    """
    return self.lines != None and self.line != None and self.currentLine != None



  def parseImplementation(self):
    """Main parsing loop. Iteratively reads errors from the lines list and adds
    them to the errors list.
    @precondition self.line is a Valgrind line.
    """

    self.readHeader()
    
    error = self.readError()
    while error != None:
      self.errors.append(error)
      error = self.readError()



  def readHeader(self): # Boolean
    """Jump past the Valgrind header. Resets the parser state if no Valgrind lines
    are found after the header.
    @return True if a Valgrind line was found after the header. False otherwise.
    @precondition self.line is a Valgrind line.
    @postcondition On True: self.line is a Valgrind line. On False: isParsing() returns false.
    """

    while self.patterns.isHeader.match(self.line) != None:
      hadAnotherLine = self.nextValgrindLine()
      if not hadAnotherLine:
        return False

    return True



  def readError(self): # ParsedError
    """Read an error from the lines list. Will skip unknown Valgrind lines until
    an error is found. Skipped lines are added to unknownErrors.
    @precondition self.line is a Valgrind line.
    """

    if not self.isParsing():
      return None

    while not self.patterns.isErrorStart(self.line):
      if len(self.line) > 0:
        self.unknownErrors.append(self.line)
      hadAnotherLine = self.nextValgrindLine()
      if not hadAnotherLine:
        return None

    error = ParsedError(self.line)

    hadAnotherLine = self.nextValgrindLine()
    if not hadAnotherLine:
      return None

    hadStacks = self.readStacks(error)
    if not hadStacks:
      return None

    return error



  def readStacks(self, error):
    # There can be up to two call stacks; a mandatory one for the error and an
    # optional one for the source.

    if self.patterns.isStackFrameTop.match(self.line) == None:
      return False

    error.setLocation(self.line)

    while self.nextValgrindLine() and self.patterns.isStackFrameCaller.match(self.line):
      error.addCaller(self.line)

    if not self.isParsing():
      return True # It is OK to run out of lines while reading callers.

    if not self.patterns.isSourceStart(self.line):
      return True # This error didn't have a source locaiton.

    error.setSourceType(self.line)

    hadAnotherLine = self.nextValgrindLine()
    if not hadAnotherLine:
      return True # This is not really a valid error, but it's close enough to be usable.

    if not self.patterns.isStackFrameTop.match(self.line):
      return True # # This is not really a valid error, but it's close enough to be usable.

    error.setSourceLocation(self.line)

    while self.nextValgrindLine() and self.patterns.isStackFrameCaller.match(self.line):
      error.addSourceCaller(self.line)

    return True



  def initFirstLine(self): # Boolean
    while not self.isValgrindLine():
      hadAnotherLine = self.nextLine()
      if not hadAnotherLine:
        return False

    idMatch = self.patterns.readId.match(self.line)
    self.id = idMatch.group(1)

    self.stripValgrindPrefix()
    return True
    



  def isValgrindLine(self): # Boolean
    return self.line != None and self.patterns.isValgrind.match(self.line) != None



  def stripValgrindPrefix(self): # None
    match = self.patterns.stripValgrind.match(self.line)
    self.line = match.group(1)
    self.line = self.line.strip()



  def nextLine(self): # Boolean
    """Updates self.line and self.currentLine to points to the next line in
    self.lines. Resets the parser's internal state if the end of self.lines is
    reached.
    """

    self.currentLine += 1
    if (self.currentLine < len(self.lines)):
      self.line = self.lines[self.currentLine]
      assert self.line != None, "Found 'None' in lines list. This is not allowed."
      return True
    else:
      self.resetState()
      return False



  def nextValgrindLine(self): # Boolean
    """Step forward through the lines until a Valgrind line is found. Resets
    the parser's internal state and returns False if the end of the list is
    reached.
    """

    hadAnotherLine = self.nextLine()
    if not hadAnotherLine:
      return False

    while not self.isValgrindLine():
      hadAnotherLine = self.nextLine()
      if not hadAnotherLine:
        return false;

    self.stripValgrindPrefix()
    return True

