from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *

from string import ascii_letters


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        total_priorities = 0
        for rucksack in raw_input:
            compartment_size = len(rucksack) // 2
            compartment_1, compartment_2 = rucksack[:compartment_size], rucksack[compartment_size:]
            common_item = set(compartment_1).intersection(compartment_2).pop()
            total_priorities += ascii_letters.index(common_item) + 1
        return total_priorities

    def solve_part_2(self, raw_input: str):
        groups = [raw_input[i:i + 3] for i in range(0, len(raw_input), 3)]
        total_priorities = 0
        for group in groups:
            common_item = set(group[0]).intersection(group[1]).intersection(group[2]).pop()
            total_priorities += ascii_letters.index(common_item) + 1
        return total_priorities
