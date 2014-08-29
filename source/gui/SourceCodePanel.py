"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import wx
import wx.stc



class SourceCodePanel(wx.Panel):
  def __init__(self, parent, initialText):
    """ A source code panel displays source code in a non-editable text area.
    @param parent - wx.Window - The GUI container that will hold the SourceCodePanel.
    @param initialText - string - Text to be displayed in the text area until changed.
    """
    wx.Panel.__init__(self, parent=parent)

    self.sourceCode = wx.stc.StyledTextCtrl(self, style=wx.TE_MULTILINE)

    if initialText != None:
      self.sourceCode.AddText(initialText)
      
    self.sourceCode.SetReadOnly(True)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.sourceCode, 1, wx.EXPAND)
    self.SetSizer(sizer)