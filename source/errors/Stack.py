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



  def __init__(self, line):
    """Create a stack frame from a Valgrind log line.
    \param line - String
    """

    address = None # String
    method = None # String
    arguments = None # String
    modifier = None # String
    fileName = None # String
    lineNumber = None # Integer
    library = None # String


    match = patterns.isAnyStackFrame.match(line)
    if match != None:
      self.fileName = match.group('fileName')
      self.lineNumber = match.group('lineNumber')
      self.library = match.group('library')
      self.modifier = match.group('modifier')
      self.address = match.group('address')
      self.method = match.group('method')
      self.arguments = match.group('arguments')



  def fileLocation(self): # String
    """Construct a human readable string describing the file location that the
    stack frame represents.
    """

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



  def fullMethod(self): # String
    """Create a human readable string describing the method that the stack frame
    represents.
    """

    ### \todo Should probably include 'modifier' here as well.
    if self.method != None and self.arguments != None:
      return self.method + self.arguments;
    elif self.method != None:
      return self.method
    else:
      return ""



  def __str__(self): # String
    return self.fileLocation() + ": " + self.fullMethod()



  def __eq__(self, other): # Boolean
    """Test if two StackFrames represents the same method. Instruction address
    is not included in the comparison.
    """

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



  def __ne__(self, other): # Boolean
    return not self.__eq__(other)





class Stack(object):
  """An ordered list of stack frames."""

  
  ## Stacks are bulit incrementally as frames are read from the file. The
  ## stack object is therefore initialized empty.
  def __init__(self):

    ## Frames are stored top-to-bottom, so  frames[0] is the method that caused
    ## the error and frames[-1] is usually the stack frame for main.
    self.frames = [] # StackFrame[]




  def setLocation(self, stackFrame): # None
    """Put the given stack frame at the top of the stack."""

    self.frames.insert(0, stackFrame);



  def addCaller(self, stackFrame): # None
    """Add another caller at the bottom of the call stack. The last addCaller
    call usually adds the stack frame for main.
    """

    self.frames.append(stackFrame)
