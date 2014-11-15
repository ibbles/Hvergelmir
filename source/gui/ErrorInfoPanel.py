"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

import wx


class ErrorInfoPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)

        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def display(self, error):
        """"""
        self.clear()
        self.text.write(error.info())

    def clear(self):
        """"""
        self.text.Clear()
