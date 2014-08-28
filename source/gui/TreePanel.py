"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import wx

class TreePanel(wx.Panel):
  """A GUI widget that displays a call graph tree."""

  def __init__(self, parent, error):
    wx.Panel.__init__(self, parent=parent)

    self.tree = wx.TreeCtrl(self)

    self.treeRoot = self.tree.AddRoot("Errors")
    self.appendToTree(self.treeRoot, error, 0)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.tree, 1, flag=wx.EXPAND)
    self.SetSizer(sizer)


  def appendToTree(self, guiTreeNode, errorTreeNode, depth): # None
    """Recursively build the GUI tree from the error tree.
    @param guiTreeNode - The GUI tree node at which the error should be inserted.
    @param errorTreeNode - SharedStackError - The error to insert into the tree.
    @param depth - integer - Current tree level. Also the index in the call stack for the current stack frame.
    """

    stackFrame = errorTreeNode.getLocation()
    title = "["+str(len(errorTreeNode.errors))+"]" + stackFrame.method + ":" + (stackFrame.lineNumber and stackFrame.lineNumber or stackFrame.address or "")
    newNode = self.tree.AppendItem(guiTreeNode, title, 1, 1, wx.TreeItemData(stackFrame))
    for error in errorTreeNode.errors:
      if error.errorStack.getNumFrames() == depth:
        self.tree.AppendItem(newNode, error.errorType, 1, 1, wx.TreeItemData(error))

    for child in errorTreeNode.children:
      self.appendToTree(newNode, child, depth+1)


