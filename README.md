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