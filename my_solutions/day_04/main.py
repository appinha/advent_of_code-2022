from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        pairs = process_input(raw_input)
        return sum(1 for ranges in pairs
            if is_contained(*ranges) or is_contained(*reversed(ranges)))

    def solve_part_2(self, raw_input: str):
        pairs = process_input(raw_input)
        return sum(1 for ranges in pairs if has_overlap(*ranges))


def process_input(raw_input: str):

    def get_ranges(pair: str):
        return [list(map(int, r.split("-"))) for r in pair.split(",")]

    return [get_ranges(pair) for pair in raw_input]


def is_contained(r1: list[int], r2: list[int]):
    return r1[0] >= r2[0] and r1[1] <= r2[1]


def has_overlap(r1: list[int], r2: list[int]):
    r1, r2 = map(set, map(lambda r: range(r[0], r[1] + 1), [r1, r2]))
    return r1.intersection(r2)
