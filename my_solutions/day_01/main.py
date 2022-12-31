from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input: str):
        calories_totals = process_input(raw_input)
        return max(calories_totals)

    def solve_part_2(self, raw_input: str):
        calories_totals = process_input(raw_input)
        return sum(heapq.nlargest(3, calories_totals))


def process_input(raw_input: str):
    return [sum(map(int, elf.split("\n"))) for elf in raw_input]
