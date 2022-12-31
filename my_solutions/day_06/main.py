from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str):
        return find_marker(raw_input, 4)

    def solve_part_2(self, raw_input: str):
        return find_marker(raw_input, 14)


def find_marker(string: str, n: int):
    for i in range(len(string) - (n - 1)):
        substring = string[i:i + n]
        if len(set(substring)) == n:
            return i + n
