# run_doctests.py
import doctest
import doctests.count_vowels
import doctests.square
import doctests.square_root

doctest.testmod(doctests.count_vowels)
doctest.testmod(doctests.square)
doctest.testmod(doctests.square_root)
