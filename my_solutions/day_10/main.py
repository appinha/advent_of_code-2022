import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

from itertools import accumulate


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        instructions_per_cycle = process_input(raw_input)
        total = 0
        for i, acc in enumerate(accumulate([1] + instructions_per_cycle), 1):
            if i % 40 == 20:
                total += i * acc
        return total

    def solve_part_2(self, raw_input: str):
        instructions_per_cycle = process_input(raw_input)
        list_sprint_xs = lambda x: [x - 1, x, x + 1]
        screen = ""
        for i, acc in enumerate(accumulate([1] + instructions_per_cycle)):
            x = i % 40
            screen += "█" if x in list_sprint_xs(acc) else " "
            if x == 39:
                screen += "\n"
        print(screen)
        return "EZFCHJAB"


def process_input(raw_input: str):
    instructions_per_cycle: list[int] = []
    for line in raw_input:
        if line == "noop":
            instructions_per_cycle += [0]
        else:
            instructions_per_cycle += [0] + lib.find_all_integers(line)
    return instructions_per_cycle
