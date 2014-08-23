"""

Classes representing a call stack. It holds data extracted from one line of a
call stack printed by Valgrind.

Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


from LineMatching import Patterns

patterns = Patterns()

class StackFrame(object):
  """A single stack frame within a call stack. Knows where in the applicaion it is."""

  address = None
  method = None
  arguments = None
  modifier = None
  fileName = None
  lineNumber = None
  library = None



  def __init__(self, line):
    """Create a stack frame from a Valgrind log line."""

    match = patterns.isAnyStackFrame.match(line)
    if match != None:
      self.fileName = match.group('fileName')
      self.lineNumber = match.group('lineNumber')
      self.library = match.group('library')
      self.modifier = match.group('modifier')
      self.address = match.group('address')
      self.method = match.group('method')
      self.arguments = match.group('arguments')



  def fileLocation(self):
    """Construct a human readable string describing the file location that the stack frame represents."""

    if self.fileName != None and self.lineNumber != None:
      return self.fileName + ":" + self.lineNumber
    elif self.fileName != None:
      return self.fileName
    elif self.library != None and self.address != None:
      return self.library + "@" + self.address
    elif self.library != None:
      return self.library
    else:
      return ""



  def fullMethod(self):
    """Create a human readable string describing the method that the stack frame represents."""

    ### \todo Should probably include 'modifier' here as well.
    if self.method != None and self.arguments != None:
      return self.method + self.arguments;
    elif self.method != None:
      return self.method
    else:
      return ""



  def __str__(self):
    return self.fileLocation() + ": " + self.fullMethod()



  def __eq__(self, other):
    """Test if two StackFrames represents the same method. Instruction address is not included in the comparison."""

    ### \todo Should perhaps look at address if 'library' is the only not-None member.
    if type(other) is type(self):
      return self.method == other.method and \
             self.arguments == other.arguments and \
             self.fileName == other.fileName and \
             self.lineNumber == other.lineNumber and \
             self.library == other.library
             # Not comparing address because that's to specific and not generally useful.
    else:
      return False;



  def __ne__(self, other):
    return not self.__eq__(other)



