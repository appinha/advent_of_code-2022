from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

from aoc_lib import X, Y


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        moves = process_input(raw_input)
        return simulate_rope(moves, 2)

    def solve_part_2(self, raw_input: str):
        moves = process_input(raw_input)
        return simulate_rope(moves, 10)


def process_input(raw_input: str):

    def get_move(s: str):
        direction, n = s.split(" ")
        return direction, int(n)

    return [get_move(line) for line in raw_input]


HEAD = 0
TAIL = -1
MOVES = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}


class Knot:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return f"({self.x},{self.y})"

    @property
    def coord(self):
        return self.x, self.y

    def move(self, direction: str):
        self.x, self.y = lib.cross_sum(self.coord, MOVES[direction])

    def follow(self, destination: Knot):
        diff = self._calc_diff(destination.coord)
        if abs(diff[X]) == 2:
            self.x += 1 if diff[X] > 0 else -1
            if abs(diff[Y]) == 1:
                self.y += diff[Y]
        if abs(diff[Y]) == 2:
            self.y += 1 if diff[Y] > 0 else -1
            if abs(diff[X]) == 1:
                self.x += diff[X]

    def _calc_diff(self, destination: Knot):
        return destination[X] - self.coord[X], destination[Y] - self.coord[Y]


def simulate_rope(moves: list[tuple[str, int]], knot_qty: int):
    rope = [Knot(0, 0) for _ in range(knot_qty)]
    visited = {rope[TAIL].coord}
    for direction, n in moves:
        for _ in range(n):
            rope[HEAD].move(direction)
            for i in range(1, len(rope)):
                rope[i].follow(rope[i - 1])
            visited.add(rope[-1].coord)
    return len(visited)
