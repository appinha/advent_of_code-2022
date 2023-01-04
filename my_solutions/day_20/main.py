from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        numbers = process_input(raw_input)
        return decrypt(numbers)

    def solve_part_2(self, raw_input: str):
        numbers = process_input(raw_input, 811589153)
        return decrypt(numbers, 10)


def process_input(raw_input: str, key=1):
    return [int(line) * key for line in raw_input]


def decrypt(numbers: list[int], mixes=1):
    length = len(numbers)
    new_indexes = [i for i in range(length)]

    for _ in range(mixes):
        for i, number in enumerate(numbers):
            if number == 0:
                continue
            curr_i = new_indexes.index(i)
            new_indexes.remove(i)
            new_i = (curr_i + number) % (length - 1)
            new_indexes.insert(new_i, i)

    new_numbers = [numbers[i] for i in new_indexes]

    zero_i = new_numbers.index(0)
    x_i, y_i, z_i = [(zero_i + n) % length for n in [1_000, 2_000, 3_000]]
    return sum([new_numbers[x_i], new_numbers[y_i], new_numbers[z_i]])
