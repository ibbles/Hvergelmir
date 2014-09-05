"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

from gui.ErrorInfoPanel import ErrorInfoPanel
from gui.SourceCodePanel import SourceCodePanel

import wx


class ErrorPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent)
    splitter = wx.SplitterWindow(self)
    self.errorInfo = ErrorInfoPanel(splitter)
    self.sourceCode = SourceCodePanel(splitter, "Select an error from the list.")
    splitter.SplitHorizontally(self.errorInfo, self.sourceCode)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(splitter, 1, wx.EXPAND)
    self.SetSizer(sizer)
