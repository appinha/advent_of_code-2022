import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input):
        return self._find_marker(raw_input, 4)

    def solve_part_2(self, raw_input):
        return self._find_marker(raw_input, 14)

    def _find_marker(self, string, n):
        for i in range(len(string) - (n - 1)):
            substring = string[i:i + n]
            if len(set(substring)) == n:
                return i + n
