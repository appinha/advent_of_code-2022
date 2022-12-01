import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input):
        ordered_total_calories = self._get_input(raw_input)
        return ordered_total_calories[0]

    def solve_part_2(self, raw_input):
        ordered_total_calories = self._get_input(raw_input)
        return sum(ordered_total_calories[:3])

    def _get_input(self, raw_input):
        total_calories = []
        for elf in raw_input:
            calories = map(int, elf.split("\n"))
            total_calories.append(sum(calories))
        return sorted(total_calories, reverse=True)
