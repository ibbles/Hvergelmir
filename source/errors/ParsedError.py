"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

from Stack import Stack
from Stack import StackFrame


class ParsedError(object):
  """A complete error parsed from the Valgrind log. Contains an eror type and
  an error call stack. May also contain a source type and source stack. The
  source is often the place where some memory related to the error was
  allocated or free'd.

  Instances of this class are created and configured by the ErrorParser.
  """


  def __init__(self, type):
    """ Create a new ParsedError with the given error type and empty call stacks.
    \param type - String - The Valgrind diagnostic line for this error.
    """
    ## The Valgrind diagnostic line, i.e. , the first line printed for this error.
    ## Must match one of the patterns tested in Patterns.isErrorStart().
    self.errorType = type # String
  
    ## A Stack object pointing out the location where the error happened.
    self.errorStack = Stack() # Stack

    ## The Valgrind description of the semantics of the source location. Not
    ## always available. Must match one of the patterns tested in
    ## Patterns.isSourceStart() if not None.
    self.sourceType = None # String

    ## Call stack describing the location of the source event. Often the
    ## location of a malloc/new or free/delete.
    self.sourceStack = Stack() # Stack



  def getStackFrame(self, index, direction): # StackFrame
    """Returns the StackFrame at the given index. Direction may be either
    Stack.FROM_TOP or Stack.FROM_BOTTOM.
    """

    return self.errorStack.getFrame(index, direction)


  def hasSameStackFrameAs(self, other, index, direction): # Boolean
    """"Test if two ParsedErrors share the same stack frame at the given index,
    when traversed in the given direction.

    \param other - ParsedError - The ParsedError instance to compare the stack frame with.
    \param index - Integer - The index of the frame to compare.
    \param direction - Stack.FROM_TOP or Stack.FROM_BOTTOM - The end of the stack that 'index' is relative to.
    """

    selfFrame = self.getStackFrame(index, direction)
    otherFrame = other.getStackFrame(index, direction)
    if myFrame == None or otherFrame == None:
      return False
    else:
      return selfFrame == otherFrame



  def display(self): # None
    """Print a longer string representation of this error to standard output."""
    print(self.info())



  def __str__(self): # String
    """Return a single line string representation of this error containing the
    error type and the stack frame at the top of the stack.
    """

    return self.type + " @ " + str(self.errorStack.getFrame(0, Stack.FROM_TOP))



  def info(self): # String
    """Return a longer string representation of this error."""
    info  = "Type: " + self.type + "\n\n"
    info += "Location: " + "\n"

    for frame in self.errorStack.frames:
      info += "    " + str(frame) + "\n"

    if self.sourceType != None:
      info += "\nSource: " + self.sourceType + "\n"
      for frame in self.sourceStack.frames:
        info += "    " + str(frame) + "\n"

    return info



  def setLocation(self, location): # None
    """Set the location where the error was detected. The 'location' string
    should match Patterns.isStackFrameTop.
    \param location - String - The first row of a Valgrind call stack print.
    """

    self.errorStack.setLocation(StackFrame(location))



  def addCaller(self, location): # None
    """Add a caller to the call stack for the error location. The 'location'
    string should match Pattens.isStackFrameCaller.
    \param location - String - A line from a Valgrind call stack print.
    """

    self.errorStack.addCaller(StackFrame(location))



  def setSourceType(self, type): # None
    self.sourceType = type;


  def setSourceLocation(self, location): # None
    self.sourceStack.setLocation(StackFrame(location))


  def addSourceCaller(self, location): # None
    self.sourceStack.addCaller(StackFrame(location))


    