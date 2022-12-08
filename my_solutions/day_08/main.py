import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input):
        trees = lib.Grid(string=raw_input, type=int)

        def is_not_visible_in_line(pos, line):
            return any(trees[pos] <= trees[lp] for lp in line)

        not_visible_trees = []
        for pos, lines in trees.orthogonal_adjacencies_by_pos.items():
            if any([not line for line in lines]):
                continue
            if all(is_not_visible_in_line(pos, line) for line in lines):
                not_visible_trees.append(pos)

        return trees.len - len(not_visible_trees)

    def solve_part_2(self, raw_input):
        trees = lib.Grid(string=raw_input, type=int)

        highest_score = 0
        for pos, lines in trees.orthogonal_adjacencies_by_pos.items():
            scores = 1
            for line in lines:
                score = 0
                for lp in line:
                    score += 1
                    if trees[pos] <= trees[lp]:
                        break
                scores *= score
            if scores > highest_score:
                highest_score = scores
        return highest_score
