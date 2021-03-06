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

        # The pathCache is a str->str dictionary that holds <file name> -> <path>
        # mappings. If a file is searched but not found then the emptry string is
        # stored in the <path>.
        self.pathCache = {}


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

        foundPath = self.findFile(path)
        if foundPath is None:
            return None

        try:
            with open(foundPath, "r") as fileHandle:
                return FileReader.readFileFile(fileHandle)
        except IOError:
            print "Could not read file '" + foundPath + "'."
            return None



    @staticmethod
    def readFileFile(fileHandle):
        """Read the contents of the given file object and return it as a list of
        string. Newlines are stripped.
        :param fileHandle: File object to read from.
        :type fileHandle: FilIO[str]
        :return: The contents of the file as a list of strings, one per line in the file..
        :rtype str list.
        """

        lines = fileHandle.read().splitlines()
        return lines



    def findFile(self, path): # string
        """Search the prefixes for a readable file. The 'path' may contain prefixes.
        For example, when give "textures/grass.png" 'findFile' may return
        "./data/graphics/GPU/textures/grass.png" if "./data" has been added as an prefix.
        :type path: str - The file to search for.
        :rtype : str - Path to a readable file found below one of the prefixes.
        """

        cached = self.pathCache.get(path)
        if cached is not None and cached != "":
            return cached  # Have the path already. Just return it.
        if cached is not None and cached == "":
            return None  # We searched for this path previously but found nothing.

        # Not in cache, do disk search.

        for prefix in self.prefixes:
            foundPath = self.findFileInDirectory(prefix, path)
            if foundPath is not None:
                # Found the file. Add its path to the path cache.
                self.pathCache[path] = foundPath
                return foundPath

        # No file with that name found. Insert empty string marker in the path cache.
        self.pathCache[path] = ""
        return None


    @staticmethod
    def findFileInDirectory(directory, path):
        """Search recursively for a readable file at the given path relative to
        the given directory.

        For example, searching for 'path' "utility/config.h" in 'directory'
        "/projects/my_project" may return "/projects/my_project/sources/include/helper/utility/config.h"
                                             |-----directory-----|----recursive part----|-----path------|


        @return string - The path to a readable file, or None of no such file exists.
        :param directory: The path to the directory where the search should start.
        :type directory: str
        :param path: The tail of the path of the wanted file.
        :type path: str
        :return Path to a readable file.
        :rtype : str
        """
        filePath = os.path.join(directory, path)
        if FileReader.isReadable(filePath):
            return filePath
        else:
            subdirectories = FileReader.getSubdirectories(directory)
            for subdirectory in subdirectories:
                foundPath = FileReader.findFileInDirectory(subdirectory, path)
                if foundPath is not None:
                    return foundPath


    @staticmethod
    def isReadable(path): # boolean
        """
        Returns True if the given path points to a readable file.
        :type path: str
        :return: bool
        """
        return os.path.isfile(path) and os.access(path, os.R_OK)


    @staticmethod
    def getSubdirectories(path):
        """ Returns a list of all immediate subdirectories within the directory at
        the given path. The list will contain the joined path, i.e. 'path' will be
        prepended before the found subdirectory name.

        :param path: The path to the director from which subdirectories should be collected.
        :return: A list of subdirectory paths found in the directory at the given path.
        """
        return [os.path.join(path, f) for f in os.listdir(path)  if os.path.isdir(os.path.join(path, f))]