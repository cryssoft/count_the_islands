Another trivial program to play with what seems to be a "leetcode" example my way.  This one uses a cellular automata-style
solver to reduce the mass of each "island" (contiguous set of 1s up/down/left/right) to a single cell then counts them in
a trivial loop.

USAGE:  count_the_islands_ca.py expected-rows expected-columns filename

There's a little input/data validation and exception handling, but production-grade code would need more.
