import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

from aoc_lib import HashGrid, NumpyGrid


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input):
        trees = HashGrid(raw_input, int)

        def is_visible_in_line(pos, line):
            for lp in line:
                if trees.map[pos] <= trees.map[lp]:
                    return False
            return True

        not_visible_trees = []
        for pos, lines in trees.orthogonal_adjacencies_by_pos.items():
            if any([not line for line in lines]):
                continue
            is_visible = any(is_visible_in_line(pos, line) for line in lines)
            if not is_visible:
                not_visible_trees.append(pos)

        return trees.len - len(not_visible_trees)

    def solve_part_2(self, raw_input):
        trees = HashGrid(raw_input, int)
        highest_score = 0
        for pos, lines in trees.orthogonal_adjacencies_by_pos.items():
            scores = []
            for line in lines:
                score = 0
                for lp in line:
                    score += 1
                    if trees.map[pos] <= trees.map[lp]:
                        break
                scores.append(score)
            if lib.prod(scores) > highest_score:
                highest_score = lib.prod(scores)
        return highest_score


