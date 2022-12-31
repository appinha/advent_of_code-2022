from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import Grid
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str):
        trees = Grid(string=raw_input, dtype=int)

        def is_not_visible_in_line(location: tuple[int, int], line: list[tuple[int, int]]):
            return any(trees[location] <= trees[lp] for lp in line)

        not_visible_trees = []
        for location, tree_lines in trees.orthogonal_neighbours_by_location.items():
            if any([not line for line in tree_lines]):
                continue
            if all(is_not_visible_in_line(location, line) for line in tree_lines):
                not_visible_trees.append(location)

        return trees.len - len(not_visible_trees)

    def solve_part_2(self, raw_input: str):
        trees = Grid(string=raw_input, dtype=int)

        highest_score = 0
        for location, tree_lines in trees.orthogonal_neighbours_by_location.items():
            scores = 1
            for line in tree_lines:
                score = 0
                for lp in line:
                    score += 1
                    if trees[location] <= trees[lp]:
                        break
                scores *= score
            if scores > highest_score:
                highest_score = scores

        return highest_score
