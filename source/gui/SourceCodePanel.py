"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import wx
import wx.stc



def appendNewline(string):
  return string+"\n"



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


  def clear(self):
    self.sourceCode.SetReadOnly(False)
    self.sourceCode.ClearAll()
    self.sourceCode.SetReadOnly(True)


  def setSourceCode(self, lines, highlightedLine): # None
    """Display 'lines'. If 'highlightedLine' is given then that line will be
    highlighted and brought into view. Line number indices are 1-based to match
    Valgrinds line numbering style.
    @param lines - string list - Content to be displayed.
    @param highlightedLine - integer - Line number to highlight. Pass 1 to highlight the first line."""

    self.sourceCode.SetReadOnly(False)
    self.sourceCode.ClearAll()
    self.sourceCode.AddText(''.join(map(appendNewline, lines)))
    if highlightedLine != None and len(lines) > highlightedLine:
      self.highlightLine(lines, highlightedLine)
    self.sourceCode.SetReadOnly(True)



  def highlightLine(self, lines, highlightedLine): # None
    ## Compensate for 1-based line number indexing.
    index = highlightedLine-1

    ## StyledTextCtrl doesn't have a line highligther, so we need to find the
    ## character indices of the wanted line.
    firstChar = 0

    ## Count the number of charactrs in the lines preceeding the wanted one.
    for i in range(0, index):
      firstChar += len(lines[i])+1

    ## Move forward past the wanted line to find the last character.
    lastChar = firstChar + len(lines[index])

    self.sourceCode.SetSelection(firstChar, lastChar)

    scrollIndex = max(index-10, 0)
    self.sourceCode.ScrollToLine(scrollIndex)

