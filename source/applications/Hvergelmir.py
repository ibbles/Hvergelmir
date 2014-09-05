"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

import os
import sys


from gui.TreePanel import TreePanel
from gui.SourceCodePanel import SourceCodePanel

from disk.FileReader import FileReader

from operations.ErrorParser import ErrorParser

from errors.ParsedError import ParsedError
from errors.SharedStackError import SharedStackError
from errors.Stack import Stack
from errors.Stack import StackFrame

import argparse
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
    if isinstance(data, StackFrame):
      stackFrame = data
    elif isinstance(data, ParsedError):
      stackFrame = data.getStackFrame(0, Stack.FROM_TOP)
    else:
      return

    filePath = stackFrame.fileName
    if filePath == None:
      return
    lines = fileReader.readFile(filePath)
    if lines == None:
      print("Could not read source code from '" + filePath + "'.")
      return
    self.sourceCode.setSouceCode(lines, int(stackFrame.lineNumber))



if __name__ == "__main__":
  
  ## Configure the command line options we support.
  parser = argparse.ArgumentParser()
  parser.add_argument("log", help="The Valgrind log file. Pass '-' to read from standard in.")
  parser.add_argument("-p", "--path", default=[], action="append", help="Directories to search for source code.")
  args = parser.parse_args()

  ## Read command line options.
  filePath = args.log
  for path in args.path:
    fileReader.addPrefix(path)


  ## Determine if we should read the Valgrind log from a file or standard in.
  if filePath == "-":
    lines = fileReader.readFile(sys.stdin)
  else:
    lines = fileReader.readFile(filePath)
    ## If we are reading from a file and the user didn't specify the --path option,
    ## then guess that source file paths are relative to the folder where the log is.
    if len(args.path) == 0:
      logDir = os.path.dirname(os.path.abspath(filePath))
      fileReader.addPrefix(logDir)

  ## Bail if we don't have any lines. The reader will have printed some error
  ## message already.
  if lines == None:
    sys.exit(1)

  ## Setup done. Launch log parsing and the GUI.
  Hvergelmir(lines)

