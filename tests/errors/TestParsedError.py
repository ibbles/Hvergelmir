"""
Tests for ParsedError.

Part of Hvergelmir, a tree based Valgrind output viewer - https://github.com/ibbles/Hvergelmir
See LICENSE for licensing information.
"""


import sys
sys.path.append("../../source")

from errors.LineMatching import Patterns
from errors.ParsedError import ParsedError


valgrindLog = [
  "==7420== Conditional jump or move depends on uninitialised value(s)",
  "==7420==    at 0x518A7A7: __printf_fp (printf_fp.c:400)",
  "==7420==    by 0x5189A52: vfprintf (vfprintf.c:1660)",
  "==7420==    by 0x51AE3C8: vsnprintf (vsnprintf.c:119)",
  "==7420==    by 0x4EBAFAF: ??? (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.19)",
  "==7420==    by 0x4EC1423: std::ostreambuf_iterator<char, std::char_traits<char> > std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >::_M_insert_float<double>(std::ostreambuf_iterator<char, std::char_traits<char> >, std::ios_base&, char, char, double) const (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.19)",
  "==7420==    by 0x4EC170F: std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >::do_put(std::ostreambuf_iterator<char, std::char_traits<char> >, std::ios_base&, char, double) const (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.19)",
  "==7420==    by 0x4ECCCA4: std::ostream& std::ostream::_M_insert<double>(double) (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.19)",
  "==7420==    by 0x400C22: printArray(double*) (errorProducingApplication.cpp:78)",
  "==7420==    by 0x400C9E: main (errorProducingApplication.cpp:92)",
  "==7420==  Uninitialised value was created by a heap allocation",
  "==7420==    at 0x4C2B800: operator new[](unsigned long) (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)",
  "==7420==    by 0x400A0B: createNewArray() (errorProducingApplication.cpp:42)",
  "==7420==    by 0x400C55: main (errorProducingApplication.cpp:85)",
]


patterns = Patterns()

lineIndex = 0

assert patterns.isErrorStart(valgrindLog[lineIndex]), "Expected error start at line '" + valgrindLog[lineIndex] + "'."
error = ParsedError(valgrindLog[lineIndex])
lineIndex += 1

assert patterns.isStackFrameTop.match(valgrindLog[lineIndex]), "Expected stack start at line '" + valgrindLog[lineIndex] + "'."
error.setLocation(valgrindLog[lineIndex])
lineIndex += 1

for i in range(0, 8):
  assert patterns.isStackFrameCaller.match(valgrindLog[lineIndex]), "Expected error stack frame caller " +str(i) + " at line '" + valgrindLog[lineIndex] + "'."
  error.addCaller(valgrindLog[lineIndex])
  lineIndex += 1

assert patterns.isSourceStart(valgrindLog[lineIndex]), "Expected the source start."
error.setSourceType(valgrindLog[lineIndex]);
lineIndex += 1

assert patterns.isStackFrameTop.match(valgrindLog[lineIndex]), "Expected stack frame top at line '" + valgrindLog[lineIndex] + "'."
error.setSourceLocation(valgrindLog[lineIndex])
lineIndex += 1

for i in range(0,2):
  assert patterns.isStackFrameCaller.match(valgrindLog[lineIndex]), "Expected source stack frame caller " + str(i) + " at line '" + valgrindLog[lineIndex] + "'."
  error.addSourceCaller(valgrindLog[lineIndex]);
  lineIndex += 1

assert lineIndex == len(valgrindLog), "Did not run out of lines when expected to. i="+str(lineIndex)+", len(lines)="+str(len(valgrindLog))
