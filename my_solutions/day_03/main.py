import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

from string import ascii_letters


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"
        self.priority = ascii_letters

    def solve_part_1(self, raw_input):
        total_priorities = 0
        for rucksack in raw_input:
            compartment_size = len(rucksack) // 2
            comp_1, comp_2 = rucksack[:compartment_size], rucksack[compartment_size:]
            common = set(comp_1).intersection(comp_2).pop()
            total_priorities += self.priority.index(common) + 1
        return total_priorities

    def solve_part_2(self, raw_input):
        groups = [raw_input[i:i + 3] for i in range(0, len(raw_input), 3)]
        total_priorities = 0
        for group in groups:
            common = set(group[0]).intersection(group[1]).intersection(group[2]).pop()
            total_priorities += self.priority.index(common) + 1
        return total_priorities
