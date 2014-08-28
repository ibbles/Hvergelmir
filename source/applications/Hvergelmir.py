"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

import os
import sys
sys.path.append(os.getcwd())


from gui.TreePanel import TreePanel

from operations.ErrorParser import ErrorParser
from errors.SharedStackError import SharedStackError
from errors.Stack import Stack

import wx




def readFileFromPath(filePath):
  try:
    if filePath == "-":
      return readFile(sys.stdin, filePath)
    else:
      with open(filePath, "r") as file:
        return readFile(file, filePath)
  except IOError:
    print "Could not read file '" + filePath + "'."
    return None


def readFile(file, filePath):
  lines = file.read().splitlines()
  if lines == None or len(lines) == 0:
    print "File '" + filePath + "' is empty."
    return None
  return lines




class Hvergelmir(object):

  def __init__(self, lines):
    ## Basic application setup.
    self.app = wx.PySimpleApp()
    self.app.frame = wx.Frame(None, title="Hvergelmir")
    self.app.frame.SetSize(wx.Size(1600, 1200))
    self.frameSizer = wx.BoxSizer(wx.VERTICAL)
    self.frameContents = wx.SplitterWindow(self.app.frame)

    ## Parse Valgrind log file.
    parser = ErrorParser()
    errors, unknowns, id = parser.parse(lines)
    self.errorTree = SharedStackError(errors, 0, Stack.FROM_BOTTOM)

    if unknowns != None:
      print("The parser didn't recognize the following error types:")
      for unknown in unknowns:
        print("  " + unknown)

    ## Create GUI.
    self.treePanelLeft = TreePanel(self.frameContents, self.errorTree)
    self.treePanelRight = TreePanel(self.frameContents, self.errorTree)
    self.frameContents.SplitVertically(self.treePanelLeft, self.treePanelRight)
    self.frameSizer.Add(self.frameContents, 1, flag=wx.EXPAND)
    self.app.frame.SetSizer(self.frameSizer)
    self.app.frame.Center()
    self.app.frame.Show()
    self.app.MainLoop()


if __name__ == "__main__":
  filePath = "-"
  if len(sys.argv) == 2:
    filePath = sys.argv[1]
  lines = readFileFromPath(filePath)
  if lines == None:
    os.exit(1)
  Hvergelmir(lines)