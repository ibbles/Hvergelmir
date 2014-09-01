"""
Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""

import os
import os.path

class FileReader(object):
  """Find and read text files. Maintains a list of directories to search in.
  The directory list initially contains '.'.
  """

  
  def __init__(self):
    self.prefixes = [] # string list.
    self.addPrefix(".")



  def addPrefix(self, prefix): # None
    """Add another folder to search for files in. The current directory (.) is implicitly added.
    @param prefix - string - Path to a folder that should be searched. Should not contain trailing '/' or '\\' or whatever.
    """

    self.prefixes.append(prefix)


  def readFile(self, fileOrPath):
    """Dispatch method. Calls either readFilePath or readFileFile depending on if
    'fileOrPath' is a string or not. If not a string, then it is assumed to have a
    read() method which returns an object with a splitlines() method that returns
    a list of strings.
    """

    if isinstance(fileOrPath, str):
      return self.readFilePath(fileOrPath)
    else:
      return self.readFileFile(fileOrPath)



  def readFilePath(self, path): # string list
    """ Read the contents of the file at 'path', prefixed with one of the prefixes. Returned as a string list or None.
    @param path - string - Path to file to read.
    @return string list with the file contents, or None if no matching readable file is found.
    """

    path = self.findFile(path)
    if path == None:
      return None

    try:
      with open(path, "r") as file:
        return self.readFileFile(file)
    except IOError:
      print "Could not read file '" + path + "'."
      return None



  def readFileFile(self, file): # string list.
    """ Read the contents of the given file object.
    @param file - file - File object to read from.
    @return string list - The contents of the file.
    """

    lines = file.read().splitlines()
    return lines



  def findFile(self, path): # string
    """Search the prefixes for a readable file."""

    for prefix in self.prefixes:
      prefixedPath = os.path.join(prefix, path)
      if self.isReadable(prefixedPath):
        return prefixedPath
    return None



  def isReadable(self, path): # boolean
    return os.path.isfile(path) and os.access(path, os.R_OK)

