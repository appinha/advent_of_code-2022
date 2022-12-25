import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input):
        result = 0
        for pair in raw_input:
            ranges = process_input(pair)
            if is_contained(*ranges) or is_contained(*reversed(ranges)):
                result += 1
        return result

    def solve_part_2(self, raw_input):
        result = 0
        for pair in raw_input:
            ranges = process_input(pair)
            if has_overlap(*ranges):
                result += 1
        return result


def process_input(pair):
    return [list(map(int, r.split("-"))) for r in pair.split(",")]


def is_contained(r1, r2):
    return r1[0] >= r2[0] and r1[1] <= r2[1]


def has_overlap(r1, r2):
    r1, r2 = map(set, map(lambda r: range(r[0], r[1] + 1), [r1, r2]))
    return r1.intersection(r2)
