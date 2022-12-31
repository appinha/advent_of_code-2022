from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        rounds = process_input(raw_input)

        # Rock == A == X: 1; Paper == B == Y: 2; Scissors == C == Z: 3
        SCORE_BY_SHAPE = {"X": 1, "Y": 2, "Z": 3}
        SCORE_BY_YOU_BY_OPPONENT = {
            "A": { "Y": 6, "X": 3, "Z": 0},
            "B": { "Z": 6, "Y": 3, "X": 0},
            "C": { "X": 6, "Z": 3, "Y": 0},
        }

        return sum(SCORE_BY_SHAPE[you] + SCORE_BY_YOU_BY_OPPONENT[opp][you] for opp, you in rounds)

    def solve_part_2(self, raw_input: str):
        rounds = process_input(raw_input)

        # Rock == A: 1; Paper == B: 2; Scissors == C: 3
        # X == lose, Y == draw, Z == win
        SCORE_BY_SHAPE = {"A": 1, "B": 2, "C": 3}
        SCORE_BY_END = {"X": 0, "Y": 3, "Z": 6}
        SHAPE_BY_END_BY_OPPONENT = {
            "A": { "X": "C", "Y": "A", "Z": "B"},
            "B": { "X": "A", "Y": "B", "Z": "C"},
            "C": { "X": "B", "Y": "C", "Z": "A"},
        }

        return sum(SCORE_BY_SHAPE[SHAPE_BY_END_BY_OPPONENT[opp][end]] + SCORE_BY_END[end]
            for opp, end in rounds)


def process_input(raw_input: str):
    return [line.split(" ") for line in raw_input]
