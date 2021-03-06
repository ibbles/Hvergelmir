"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

import os
import sys


from gui.TreePanel import TreePanel
from gui.ErrorPanel import ErrorPanel

from disk.FileReader import FileReader

from operations.ErrorParser import ErrorParser


from errors.SharedStackError import SharedStackError
from errors.Stack import Stack

import argparse
import wx


fileReader = FileReader()


class Hvergelmir(object):
    """"""

    def __init__(self, lines):
        """"""
        ## Basic application setup.
        self.app = wx.PySimpleApp()
        self.app.frame = wx.Frame(None, title="Hvergelmir")
        self.app.frame.SetSize(wx.Size(1200, 900))
        self.app.frame.CreateStatusBar(1)
        self.frameSizer = wx.BoxSizer(wx.VERTICAL)
        self.frameContents = wx.SplitterWindow(self.app.frame)

        ## Parse Valgrind log file.
        parser = ErrorParser()
        errors, unknowns, pid = parser.parse(lines)
        if errors is None:
            print("Could not read any errors.")
            sys.exit(1)

        self.errorTreeFromBottom = SharedStackError(errors, 0, Stack.FROM_BOTTOM)
        self.errorTreeFromTop = SharedStackError(errors, 0, Stack.FROM_TOP)

        if unknowns is not None:
            print("The parser didn't recognize the following error types:")
            for unknown in unknowns:
                print("  " + unknown)

        ## Create GUI.
        self.treePanel = TreePanel(self.frameContents, self.errorTreeFromBottom, self.errorTreeFromTop)
        self.errorPanel = ErrorPanel(self.frameContents)
        self.frameContents.SplitVertically(self.treePanel, self.errorPanel)
        self.frameSizer.Add(self.frameContents, 1, flag=wx.EXPAND)
        self.app.frame.SetSizer(self.frameSizer)
        self.app.frame.Center()
        self.app.frame.Show()

        ## Define GUI callbacks.
        self.treePanel.setItemSelectedCallback(self.treeItemSelected)

        self.errorPanel.sourceCode.setSourceCode(["Select an error from the list."], None)

        self.app.MainLoop()



    def treeItemSelected(self, data):
        """ Called by the TreePanel when an item is selected. The argument is the
        data that was stored in the selected item. Usually a


        :param data: TreeItemData
        """
        self.errorPanel.errorInfo.clear()

        nearestSourceStackFrame = data.nearestSourceStackFrame
        error = data.parsedError  # ParsedError instance, or None.

        if error is not None:
            self.errorPanel.errorInfo.display(error)

        sourceFilePath = nearestSourceStackFrame.fileName
        if sourceFilePath is None:
            errorMessage = "Unknown file location: " + str(nearestSourceStackFrame.fileName);
            self.setStatusText(errorMessage)
            self.errorPanel.sourceCode.setSourceCode([errorMessage], None)
            return

        lines = fileReader.readFile(sourceFilePath)
        if lines is None:
            errorMessage = "Could not read source code from '" + sourceFilePath + "'.";
            self.setStatusText(errorMessage)
            self.errorPanel.sourceCode.setSourceCode([
                errorMessage,
                "Use the --path command line argument to add additional search directories."],
                None)
            return

        self.errorPanel.sourceCode.setSourceCode(lines, int(nearestSourceStackFrame.lineNumber))

        self.setStatusText(sourceFilePath)


    def setStatusText(self, text):
        if self.app.frame.GetStatusBar().GetStatusText(0) != text:
            self.app.frame.SetStatusText(text, 0)


if __name__ == "__main__":
    """"""

    ## Configure the command line options we support.
    argParser = argparse.ArgumentParser()
    argParser.add_argument("log", help="The Valgrind log file. Pass '-' to read from standard in.")
    argParser.add_argument("-p", "--path", default=[], action="append", help="Directories to search for source code.")
    args = argParser.parse_args()

    ## Read command line options.
    filePath = args.log
    for path in args.path:
        fileReader.addPrefix(path)

    ## Determine if we should read the Valgrind log from a file or standard in.
    if filePath == "-":
        fileLines = fileReader.readFile(sys.stdin)
    else:
        fileLines = fileReader.readFile(filePath)
        ## If we are reading from a file and the user didn't specify the --path option,
        ## then guess that source file paths are relative to the folder where the log is.
        if len(args.path) == 0:
            logDir = os.path.dirname(os.path.abspath(filePath))
            fileReader.addPrefix(logDir)

    ## Bail if we don't have any lines. The reader will have printed some error
    ## message already.
    if fileLines is None:
        sys.exit(1)

    ## Setup done. Launch log parsing and the GUI.
    Hvergelmir(fileLines)
