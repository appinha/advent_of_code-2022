import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input):
        ordered_elves = self._get_input(raw_input)
        return sum(ordered_elves[-1:])

    def solve_part_2(self, raw_input):
        ordered_elves = self._get_input(raw_input)
        return sum(ordered_elves[-3:])

    def _get_input(self, raw_input):
        elves = []
        for elf in raw_input:
            calories = elf.split("\n")
            total_calories = sum([int(cal) for cal in calories if cal])
            elves.append(total_calories)
        return sorted(elves)
