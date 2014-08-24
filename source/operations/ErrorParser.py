"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

from errors.LineMatching import Patterns

class ErrorParser(object):
  """Converts a list of strings, the Valgrind log, to a list of ParsedErrors."""

  def __init__(self):
    self.resetState()



  def parse(self, lines): # (ParsedError list, string list)
    """Parser ParsedErrors from the given line list. All elements of 'lines'
    must be string-like. None elements are not allowed.
    @param lines - String list - The contents of a Valgrind log.
    @return (ParsedError list, string list) tuple containing the errors found
            and a list of unknown valgrind lines, or None if there was an error
            before any errors could be read.
    """

    setupSuccessful = self.setupState(lines)
    if not setupSuccessful:
      return None

    self.parseImplementation()

    errorList = self.errors
    unknownErrors = self.unknownErrors
    self.resetState()
    return  (errorList, unknownErrors)



  def resetState(self): # None
    """Prepare the parser for a new round of parsing. The parser is placed in a
    dormant state, waiting for the next call to parse().
    """

    if self.patterns == None:
      self.patterns = Patterns()
    self.errors = None # ParsedError list.
    self.unknownErrors = None # String list. Lines that the parser didn't recognize.
    self.lines = None # String list. Provided by user.
    self.line = None # String. One of the string in 'lines'. Is always either None or a Valgrind line.
    self.currentLine = None # Integer. The index of 'line' in 'lines'.



  def setupState(self, lines): # Boolean
    """Prepare the parser for parsing from the given string list."""

    if line == None or len(lines) == 0:
      return False

    self.errors = []
    self.unknownErrors = []

    self.lines = lines
    self.currentLine = 0
    self.line = self.lines[self.currentLine]
    return self.ensureOnValgrindLine()



  def isParsing(self): # Boolean
    """Returns True if the parser is valid for continued parsing. Calling
    resetState will cause future calls to isParsing to return False until
    setupState is called.
    """
    return self.lines != None and self.line != None and self.currentLine != None



  def parseImplementation():
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
    while not self.patterns.isErrorStart(self.line):
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
    pass



  def ensureOnValgrindLine(self): # Boolean
    if self.isValgrindLine():
      self.stripValgrindPrefix()
      return True
    else:
      return self.nextValgrindLine()



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

    hadAnotherLine = self.nextLine():
    if not hadAnotherLine:
      return False

    while not self.isValgrindLine():
      hadAnotherLine = self.nextLine()
      if not hadAnotherLine:
        return false;

    self.stripValgrindPrefix()

