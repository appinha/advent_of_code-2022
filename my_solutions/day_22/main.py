from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL, Grid
from aoc_lib.imports import *


PRINT_GRID = False


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input: str):
        grid, path = process_input(raw_input)
        return walk_on_board(grid, path, part=1)

    def solve_part_2(self, raw_input: str):
        grid, path = process_input(raw_input)
        return walk_on_board(grid, path, part=2, is_testing=self.is_testing)


Location = tuple[int, int]
Direction = tuple[str, Location]


E, S, W, N = (">", (0, 1)), ("v", (1, 0)), ("<", (0, -1)), ("^", (-1, 0))
CHAR, LOC = 0, 1


def process_input(raw_input: str):

    def get_grid(raw_grid: str):
        rows = raw_grid.split("\n")
        cols_len = max([len(row) for row in rows])
        grid = Grid(shape=(len(rows), cols_len), fill_value=" ")
        for row, line in enumerate(rows):
            for col, char in enumerate(list(line)):
                grid[(row, col)] = char
        return grid

    def get_path(raw_path: str):
        convert_int = lambda s: int(s) if s.isdigit() else s
        return list(map(convert_int, re.findall(r'\d+|[RL]', raw_path)))

    raw_grid, raw_path = raw_input
    return get_grid(raw_grid), get_path(raw_path)


def part_1_funcs():

    def must_wrap(grid: Grid, next_location: Location):
        return not grid.has_location(next_location) or grid[next_location] == " "

    def wrap(grid: Grid, curr_location: Location, direction: Direction):
        curr_row, curr_col = curr_location
        dim = ROW if direction in [N, S] else COL
        limit = min if direction in [S, E] else max

        get_location = lambda i: (i, curr_col) if direction in [N, S] else (curr_row, i)

        next_i = limit([i for i in range(grid.shape[dim]) if grid[get_location(i)] != " "])

        return get_location(next_i)

    return must_wrap, wrap


def part_2_funcs(is_testing: bool):

    LIMITS = [50, 100, 150, 200]  if not is_testing else [4, 8, 12, 16]
    WRAPS = {
        (1, W): (E, lambda row, col: ((LIMITS[2] - 1) - row, 0)),
        (1, N): (E, lambda row, col: (col + (LIMITS[1]), 0)),
        (2, E): (W, lambda row, col: ((LIMITS[2] - 1) - row, LIMITS[1] - 1)),
        (2, S): (W, lambda row, col: (col - (LIMITS[0]), LIMITS[1] - 1)),
        (2, N): (N, lambda row, col: ((LIMITS[3] - 1), col - (LIMITS[1]))),
        (3, E): (N, lambda row, col: ((LIMITS[0] - 1), row + (LIMITS[0]))),
        (3, W): (S, lambda row, col: ((LIMITS[1]), row - (LIMITS[0]))),
        (4, E): (W, lambda row, col: ((LIMITS[2] - 1) - row, (LIMITS[2] - 1))),
        (4, S): (W, lambda row, col: ((LIMITS[1]) + col, (LIMITS[0] - 1))),
        (5, W): (E, lambda row, col: ((LIMITS[2] - 1) - row, (LIMITS[0]))),
        (5, N): (E, lambda row, col: ((LIMITS[0]) + col, (LIMITS[0]))),
        (6, E): (N, lambda row, col: ((LIMITS[2] - 1), row - (LIMITS[1]))),
        (6, S): (S, lambda row, col: (0, col + (LIMITS[1]))),
        (6, W): (S, lambda row, col: (0, row - (LIMITS[1]))),
    }

    def find_face(location: Location):

        #        A     B     C
        #           /-----:-----\
        #  A        |  1  |  2  |
        #           :-----:-----/
        #  B        |  3  |
        #     /-----:-----:
        #  C  |  5  |  4  |
        #     :-----:-----/
        #  D  |  6  |
        #     \-----/

        face_by_quadrants = {"AB": 1, "AC": 2, "BB": 3, "CB": 4, "CA": 5, "DA": 6}

        def find_quadrant(i: int):
            if         0 <= i < LIMITS[0]: return "A"
            if LIMITS[0] <= i < LIMITS[1]: return "B"
            if LIMITS[1] <= i < LIMITS[2]: return "C"
            if LIMITS[2] <= i < LIMITS[3]: return "D"

        quadrants = "".join([find_quadrant(i) for i in location])
        return face_by_quadrants[quadrants]

    def must_wrap(
        grid: Grid, curr_location: Location, next_location: Location, direction: Direction
    ):

        def is_in_border(location: Location):
            border_indexes = [0] + LIMITS + [limit - 1 for limit in LIMITS]
            return any([i in border_indexes for i in location])

        def is_not_in_face(location: Location):
            return not grid.has_location(location) or grid[location] == " "

        return is_in_border(curr_location) and \
            is_not_in_face(next_location) and (find_face(curr_location), direction) in WRAPS

    def wrap(grid: Grid, curr_location: Location, directions: list[Direction]):

        def rotate_directions_until(new_direction: Direction):
            new_direction_i = directions.index(new_direction)
            directions.rotate(-new_direction_i)

        new_direction, conversion_f = WRAPS[(find_face(curr_location), directions[0])]
        next_location = conversion_f(*curr_location)
        if grid[next_location] != "#":
            rotate_directions_until(new_direction)
        return next_location

    return must_wrap, wrap


def walk_on_board(grid: Grid, path: list[int | str], part: int, is_testing=False):

    def mark_grid(location: Location, char: str):
        grid[location] = char

    match part:
        case 1:
            must_wrap_1, wrap_1 = part_1_funcs()
            must_wrap = lambda _, next_location: must_wrap_1(grid, next_location)
            wrap = lambda curr_location: wrap_1(grid, curr_location, directions[0])
        case 2:
            must_wrap_2, wrap_2 = part_2_funcs(is_testing)
            must_wrap = lambda curr_location, next_location: must_wrap_2(
                grid, curr_location, next_location, directions[0])
            wrap = lambda curr_location: wrap_2(grid, curr_location, directions)

    directions = Deque([E, S, W, N])
    curr_location = (0, grid.tolist()[0].index(".")) # starts at first dot character of first row
    mark_grid(curr_location, directions[0][CHAR])

    for step in path:
        if step == "L":
            directions.rotate(1)
        elif step == "R":
            directions.rotate(-1)
        else:
            for _ in range(step):
                next_location = lib.cross_sum(curr_location, directions[0][LOC])
                if must_wrap(curr_location, next_location):
                    next_location = wrap(curr_location)

                if grid[next_location] == "#":
                    break

                curr_location = next_location
                mark_grid(curr_location, directions[0][CHAR])

    print_grid(grid)
    row, col = lib.cross_sum(curr_location, (1, 1))
    return 1_000 * row + 4 * col + [E, S, W, N].index(directions[0])


def print_grid(grid: Grid):
    if PRINT_GRID:
        lib.pretty_print_grid(grid.tolist())
        print()
