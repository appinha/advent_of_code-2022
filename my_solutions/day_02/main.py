import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input):
        # Rock == A == X: 1; Paper == B == Y: 2; Scissors == C == Z: 3
        score_by_shape = {"X": 1, "Y": 2, "Z": 3}
        score_by_you_by_opponent = {
            "A": { "Y": 6, "X": 3, "Z": 0},
            "B": { "Z": 6, "Y": 3, "X": 0},
            "C": { "X": 6, "Z": 3, "Y": 0},
        }

        total_score = 0
        for round in raw_input:
            opp, you = round.split(" ")
            total_score += score_by_shape[you] + score_by_you_by_opponent[opp][you]
        return total_score

    def solve_part_2(self, raw_input):
        # Rock == A: 1; Paper == B: 2; Scissors == C: 3
        # X == lose, Y == draw, Z == win
        score_by_shape = {"A": 1, "B": 2, "C": 3}
        score_by_end = {"X": 0, "Y": 3, "Z": 6}
        shape_by_end_by_opponent = {
            "A": { "X": "C", "Y": "A", "Z": "B"},
            "B": { "X": "A", "Y": "B", "Z": "C"},
            "C": { "X": "B", "Y": "C", "Z": "A"},
        }

        total_score = 0
        for round in raw_input:
            opp, end = round.split(" ")
            your_shape = shape_by_end_by_opponent[opp][end]
            total_score += score_by_shape[your_shape] + score_by_end[end]
        return total_score
