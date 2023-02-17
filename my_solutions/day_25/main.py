from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        return functools.reduce(sum_snafu, raw_input)

    def solve_part_2(self, raw_input: str):
        ...


def process_input(raw_input: str):
    return [snafu_to_decimal(snafu) for snafu in raw_input]


def sum_snafu(a, b):

    def sum_digit(a, b):
        match a, b:
            case '0',  x : return  x , ''
            case '1', '=': return '-', ''
            case '1', '-': return '0', ''
            case '1', '1': return '2', ''
            case '2', '=': return '0', ''
            case '2', '-': return '1', ''
            case '2', '1': return '=', '1'
            case '2', '2': return '-', '1'
            case '=', '=': return '1', '-'
            case '=', '-': return '2', '-'
            case '-', '-': return '=', ''
        return sum_digit(b, a)

    match a, b:
        case '', '': return ''
        case a , '': return a
        case '',  b: return b
    x, r = sum_digit(a[-1], b[-1])
    return sum_snafu(r, sum_snafu(a[:-1], b[:-1])) + x


SNAFU_DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}



def snafu_to_decimal(snafu: str):
        decimal = 0
        for i, digit in enumerate(reversed(snafu)):
            decimal += (5 ** i) * SNAFU_DIGITS[digit]
        return decimal
