Hvergelmir
==========

Valgrind log viewer that merges shared stack segments of reported errors and
presents the result as a tree.


## Purpose ##

Sometimes Valgrind reports a lot of errors and scrolling through a long list of
call stacks can get a bit overwhelming. By merging shared stack frame Hvergelmir
allows the user to selectively walk down the call tree from main towards the
errors in the leaves and ignore branches that currently aren't of interest. Its
purpose is to give a bit of overview of where the errors are occurring.


## Usage ##

For those with access to bash, the main application is started using the
Hvergelmir script in the root directory. It can also be started manually by
adding the full path to the /source directory to the PYTHONPATH environment
variable and then running 'python ./applications/Hvergelmir.py'.

Hvergelmir needs a Valgrind log to read error messages from and it is passed as
a command line arguments. The log can be either a file on disk, or read from
standard in. In the latter case, pass '-' as the command line argument.

```
Hvergelmir> valgrind <valgrind options> <application> <application options> 2>"valgrind.log"
Hvergelmir> ./Hvergelmir "valgrind.log"
```

or

```
Hvergelmir> valgrind <valgrind options> <application> <application options> 2>&1 | ./Hvergelmir "-"
```

The Valgrind log may contain source code locations for the reported
errors. Hvergelmir will display read and display the source files if it can find
them. Directories where Hvergelmir will search for the source files is specified
using the "-p" or "--path" command line arguments.


## Timeline ##

* 0.1.0 Read a Valgrind log and print a list of errors to standard out.
* 0.2.0 Mergeing of call stacks. Recursive printing to standard out.
* 0.3.0 GUI showing the call stack tree, source code with the offending line highlighted and the complete Valgrind output for the selected error.
* 0.4.0 Additional features. Suggestions are welcome. Here follows a list of suggestions.
  * Opening Valgrind logs from within the application.
  * Opening files in external editor.
  * Syntax highlighting in the code viewer.
  * File editing in the code viewer.
  * Running Valgrind from within the application.
  * Embeddable GUI widgets for third-party IDEs.
  * Process selection. Use the ==ID== markers in the Valgrind log to select only the lines belonging to a given ID.
* 1.0.0 Public release.



## File organization ##

The source code for the main application is located in /source. It is split into
/source/errors, which handles error parsing and storage, /source/operations,
which contains classes for error manipulation, and /source/gui, which contains
GUI widgets. Source files intended to be runnable are stored in
/source/applications.

The source code for the unit tests are in /tests. The tests directory contains
subdirectories mirroring the /source directory, except for
/source/applications. Each subdirectory contains a test source file for each
source file in subdirectories of /source.

## Dependencies ##

Developed using python version 2.7.6.

The following import statements for external libraryes are used.

* argparse
* os
* os.path
* re
* sys
* wx
* wx.stc

On Ubuntu 18.04 the package containing the wx library is called `python-wxgtk3.0`.

## Issues ##

Don't know how to properly parse a Valgrind log file. The current approach uses
regular expression based string matching and substring extraction. Not sure if
this will hold all the way. Also, I don't have a complete listing of all output
Valgrind can produce so I have no way of knowing if the set of regular
expressions I have are complete or even if any one of them is correct. Perhaps
there is a library for this.

