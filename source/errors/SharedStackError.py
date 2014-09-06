"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

from Stack import Stack
from Stack import StackFrame


def getNumErrors(sharedStackError):
  """Returns the number of errors in a SharedStackError."""
  return len(sharedStackError.errors)



class SharedStackError(object):
  """Represents a position in the call stack tree. Maintains a list of all errors
  whose call stack passes through that point.
  """

  def __init__(self, errors, stackFramesShared, direction):

    """Create a SharedStackError from the errors list. Will recursively create
    its own children, so the entire tree is created with this SharedStackError
    as the root.
    @param error - ParsedError list
    @param stackFramesShared - Integer - The index of the stack frame that is known to be equal among all errors.
    @direction The side of the stack that is shared. Either Stack.FROM_TOP or Stack.FROM_BOTTOM.
    @precondition All stack frames with index < stackFramesShared are equal among all elements of 'errors'.
    """

    ## The Valgrind errors that has a call stack that passes through this
    ## point in the call stack tree. They all have the same call stack up to
    ## this point.
    self.errors = errors[:] # ParsedError list.

    ## A list of SharedStackErrors representing the branches off of this stack
    ## path. Each child's 'errors' list contains a subset of this
    ## SharedStackError's 'errors' list, and each child's 'stackFramesShared'
    ## is one greater that this SharedStackError's 'stackFramesShared'.
    self.children = [] # SharedStackError list.

    ## The number of stack frames that are shared up to this point.
    self.stackFramesShared = stackFramesShared # Integer

    ## The side of the call stack that is shared.
    self.direction = direction # Integer. Either Stack.FROM_BOTTOM or Stack.FROM_TOP.


    self.createChildren()
    self.children.sort(key=getNumErrors, reverse=True)


  def createChildren(self):
    ## We will be picking a list appart, and don't want that list to be the instance variable.
    consumableErrors = self.errors[:]

    while len(consumableErrors) > 0:
      pivot = consumableErrors[0]
      errorsSharingStackWithPivot = [error for error in consumableErrors if self.shouldConsumeNow(error, pivot, self.stackFramesShared, self.direction)]
      consumableErrors[:] =         [error for error in consumableErrors if self.stillConsumable( error, pivot, self.stackFramesShared, self.direction)]

      if len(errorsSharingStackWithPivot) > 0:
        self.addChild(SharedStackError(errorsSharingStackWithPivot, self.stackFramesShared+1, self.direction))


  def shouldConsumeNow(self, error, pivot, stackFramesShared, direction):
    return error.hasSameStackFrameAs(pivot, stackFramesShared, direction)


  def stillConsumable(self, error, pivot, stackFramesShared, direction):
    wasJustConsumed = self.shouldConsumeNow(error, pivot, stackFramesShared, direction)
    isOutOfStack = error.getStackFrame(stackFramesShared, direction) == None
    return not wasJustConsumed and not isOutOfStack



  def addChild(self, child):
    self.children.append(child)



  def getLocation(self): # StackFrame
    if self.stackFramesShared > 0:
      return self.errors[0].getStackFrame(self.stackFramesShared-1, self.direction)
    else:
      leafLocation = StackFrame("")
      if self.direction == Stack.FROM_BOTTOM:
        leafLocation.method = "<Below main>"
      else:
        leafLocation.method = "<Stack top>"
      return leafLocation;



  def getNearestSourceLocation(self): # StackFrame
    if self.stackFramesShared > 0:
      index = self.stackFramesShared-1
      frame = self.errors[0].getStackFrame(index, self.direction)
      while frame != None and frame.fileName == None:
        index -= 1
        frame = self.errors[0].getStackFrame(index, self.direction)

      return frame
    else:
      return self.getLocation()


  def printTree(self, depth = 0):
    print(" "*depth + str(self.getLocation()))

    for error in self.errors:
      if len(error.errorStack.frames) == depth:
        print(" "*(depth+1) + str(error))

    for child in self.children:
      child.printTree(depth+1)