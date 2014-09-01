"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

import os
import sys
sys.path.append(os.getcwd())


from gui.TreePanel import TreePanel
from gui.SourceCodePanel import SourceCodePanel

from disk.FileReader import FileReader

from operations.ErrorParser import ErrorParser

from errors.ParsedError import ParsedError
from errors.SharedStackError import SharedStackError
from errors.Stack import Stack
from errors.Stack import StackFrame

import wx


fileReader = FileReader()



class Hvergelmir(object):

  def __init__(self, lines):
    ## Basic application setup.
    self.app = wx.PySimpleApp()
    self.app.frame = wx.Frame(None, title="Hvergelmir")
    self.app.frame.SetSize(wx.Size(1200, 900))
    self.frameSizer = wx.BoxSizer(wx.VERTICAL)
    self.frameContents = wx.SplitterWindow(self.app.frame)

    ## Parse Valgrind log file.
    parser = ErrorParser()
    errors, unknowns, id = parser.parse(lines)
    if errors == None:
      print("Could not read any errors.")
      sys.exit(1)


    self.errorTree = SharedStackError(errors, 0, Stack.FROM_BOTTOM)

    if unknowns != None:
      print("The parser didn't recognize the following error types:")
      for unknown in unknowns:
        print("  " + unknown)

    ## Create GUI.
    self.treePanel = TreePanel(self.frameContents, self.errorTree)
    self.sourceCode = SourceCodePanel(self.frameContents, "Select an error from the list.")
    self.frameContents.SplitVertically(self.treePanel, self.sourceCode)
    self.frameSizer.Add(self.frameContents, 1, flag=wx.EXPAND)
    self.app.frame.SetSizer(self.frameSizer)
    self.app.frame.Center()
    self.app.frame.Show()

    ## Define GUI callbacks.
    self.treePanel.setItemSelectedCallback(self.treeItemSelected)

    self.app.MainLoop()


  def treeItemSelected(self, data):
    print("Got tree data.")
    if isinstance(data, StackFrame):
      stackFrame = data
    elif isinstance(data, ParsedError):
      stackFrame = data.getStackFrame(0, Stack.FROM_TOP)
    else:
      print("Is not a know type.")
      return

    filePath = stackFrame.fileName
    if filePath == None:
      print("The stack frame doesn't have a file name")
      return
    print("Reading source from '" + filePath + "'.")
    lines = fileReader.readFile(filePath)
    if lines == None:
      print("Could not read source code from '" + filePath + "'.")
      return
    print("Got " + str(len(lines)) + " lines of source code.")



if __name__ == "__main__":
  executableName = "Hvergelmir" ## How can I figure out the real name? It may be a bash script calling Python.
  if len(sys.argv) != 2:
    print("Usage: " + executableName + " <valgrind log> ")
    print("or")
    print("       " + "valgrind <valgrind options> <application> <application options> | " + executableName + " -")
    sys.exit(1)

  filePath = sys.argv[1]

  if filePath == "-":
    lines = fileReader.readFile(sys.stdin)
  else:
    lines = fileReader.readFile(filePath)
  if lines == None:
    sys.exit(1)
  Hvergelmir(lines)