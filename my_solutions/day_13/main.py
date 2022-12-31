from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input: str):
        pairs_of_packets = process_input(raw_input)
        return sum(i
            for i, [left, right] in enumerate(pairs_of_packets, 1)
            if compare(left, right) <= 0)

    def solve_part_2(self, raw_input: str):
        dividers = [[[2]], [[6]]]
        packets = lib.flatten_list(process_input(raw_input)) + dividers
        sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))
        return math.prod(i
            for i, packet in enumerate(sorted_packets, 1)
            if packet in dividers)


def process_input(raw_input: str):
    return [list(map(ast.literal_eval, pair.split("\n"))) for pair in raw_input]


def compare(left: int | list, right: int | list):
    match left, right:
        case int(), int():
            return left - right
        case list(), int():
            right = [right]
        case int(), list():
            left = [left]
    return next(
        (result for result in map(compare, left, right) if result),
        len(left) - len(right)  # default
    )
