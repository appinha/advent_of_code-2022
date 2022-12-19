import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

import copy
from typing import Deque, NamedTuple

SHOULD_PRINT = False
PRINT_HEIGHT = 10


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input):
        jets = lib.cycle(list(raw_input))
        return play_tetris(jets, 2022)

    def solve_part_2(self, raw_input):
        jets = lib.cycle(list(raw_input))
        return play_tetris(jets, 100_000_000)
        # return play_tetris(jets, 1_000_000_000_000)


def play_tetris(jets, max_rocks):
    rocks = lib.cycle([HOR_LINE, CROSS, L_SHAPE, VER_LINE, SQUARE])
    tower = Deque([list("+-------+")])
    rock_count = 0
    can_drop = False

    def insert_rock(tower: Deque, rock):
        new = Deque(copy.deepcopy(rock.initial)) + Deque([list(EMPTY_LINE) for _ in range(3)])
        tower.extendleft(reversed(new))
        return tower

    while True:

        if not can_drop:
            rock_count += 1
            if rock_count % 100_000 == 0:
                print(rock_count)
            if len(tower) > 6 and \
                "".join(tower[-2]) == "".join(tower[2]) and \
                "".join(tower[-3]) == "".join(tower[1]):
                # "".join(tower[-4]) == "".join(tower[0]):
                print("".join(tower[0]), "".join(tower[-4]))
                print("".join(tower[1]), "".join(tower[-3]))
                print("".join(tower[2]), "".join(tower[-2]))
                print("len:", len(tower) - 1)
                return len(tower) - 1  # minus the floor
            if rock_count == max_rocks + 1:
                return len(tower) - 1  # minus the floor
            rock = next(rocks)
            tower = insert_rock(tower, rock)
            print_grid(tower, SHOULD_PRINT)

        jet = next(jets)
        move_rock(tower, rock, jet)
        can_drop = move_rock(tower, rock, "v")


def move_rock(tower, rock, direction):
    if SHOULD_PRINT:
        print("\ndirection:", direction)

    def check(chars):
        return all([char not in ["#", "-", "|"] for char in chars])

    def find_cols(row):
        return [col for col, char in enumerate(tower[row]) if char == "@"]

    z = 0
    while not find_cols(z):
        z += 1

    can_drop = True
    if direction == "v":
        if rock.name == "hor_line":
            cols = find_cols(z + 0)
            if check([tower[z + 1][col] for col in cols]):
                for col in cols:
                    tower[z + 0][col] = "."
                    tower[z + 1][col] = "@"
            else:
                can_drop = False
        if rock.name == "cross":
            left, center, right = find_cols(z + 1)
            if check([tower[z + 2][left], tower[z + 3][center], tower[z + 2][right]]):
                tower[z + 1][left] = "."
                tower[z + 0][center] = "."
                tower[z + 1][right] = "."
                tower[z + 2][left] = "@"
                tower[z + 3][center] = "@"
                tower[z + 2][right] = "@"
            else:
                can_drop = False
        if rock.name == "l_shape":
            cols = find_cols(z + 2)
            right = cols[-1]
            if check([tower[z + 3][col] for col in cols]):
                for col in cols:
                    tower[z + 2][col] = "."
                    tower[z + 3][col] = "@"
                tower[z + 0][right] = "."
                tower[z + 2][right] = "@"
            else:
                can_drop = False
        if rock.name == "ver_line":
            center = find_cols(z + 0)[0]
            if check([tower[z + 4][center]]):
                tower[z + 0][center] = "."
                tower[z + 4][center] = "@"
            else:
                can_drop = False
        if rock.name == "square":
            cols = find_cols(z + 0)
            if check([tower[z + 2][col] for col in cols]):
                for col in cols:
                    tower[z + 0][col] = "."
                    tower[z + 2][col] = "@"
            else:
                can_drop = False

    elif direction == ">":
        if rock.name == "hor_line":
            left, _, _, right = find_cols(z + 0)
            if check([tower[z + 0][right + 1]]):
                tower[z + 0][left] = "."
                tower[z + 0][right + 1] = "@"
        if rock.name == "cross":
            center = find_cols(z + 0)[0]
            if check([tower[z + 0][center + 1], tower[z + 1][center + 2], tower[z + 2][center + 1]]):
                tower[z + 0][center] = "."
                tower[z + 0][center + 1] = "@"
                tower[z + 1][center - 1] = "."
                tower[z + 1][center + 2] = "@"
                tower[z + 2][center] = "."
                tower[z + 2][center + 1] = "@"
        if rock.name == "l_shape":
            right = find_cols(z + 0)[0]
            if check([tower[z + row][right + 1] for row in range(3)]):
                tower[z + 0][right] = "."
                tower[z + 0][right + 1] = "@"
                tower[z + 1][right] = "."
                tower[z + 1][right + 1] = "@"
                tower[z + 2][right - 2] = "."
                tower[z + 2][right + 1] = "@"
        if rock.name == "ver_line":
            center = find_cols(z + 0)[0]
            if check([tower[z + row][center + 1] for row in range(4)]):
                for row in range(4):
                    tower[z + row][center] = "."
                    tower[z + row][center + 1] = "@"
        if rock.name == "square":
            left, right = find_cols(z + 0)
            if check([tower[z + row][right + 1] for row in range(2)]):
                for row in range(2):
                    tower[z + row][left] = "."
                    tower[z + row][right + 1] = "@"

    elif direction == "<":
        if rock.name == "hor_line":
            left, _, _, right = find_cols(z + 0)
            if check([tower[z + 0][left - 1]]):
                tower[z + 0][right] = "."
                tower[z + 0][left - 1] = "@"
        if rock.name == "cross":
            center = find_cols(z + 0)[0]
            if check([tower[z + 0][center - 1], tower[z + 1][center - 2], tower[z + 2][center - 1]]):
                tower[z + 0][center] = "."
                tower[z + 0][center - 1] = "@"
                tower[z + 1][center + 1] = "."
                tower[z + 1][center - 2] = "@"
                tower[z + 2][center] = "."
                tower[z + 2][center - 1] = "@"
        if rock.name == "l_shape":
            left, center, right = find_cols(z + 2)
            if check([tower[z + 0][right - 1], tower[z + 1][right - 1], tower[z + 2][left - 1]]):
                tower[z + 0][right] = "."
                tower[z + 0][right - 1] = "@"
                tower[z + 1][right] = "."
                tower[z + 1][right - 1] = "@"
                tower[z + 2][right] = "."
                tower[z + 2][left - 1] = "@"
        if rock.name == "ver_line":
            center = find_cols(z + 0)[0]
            if check([tower[z + row][center - 1] for row in range(4)]):
                for row in range(4):
                    tower[z + row][center] = "."
                    tower[z + row][center - 1] = "@"
        if rock.name == "square":
            left, right = find_cols(z + 0)
            if check([tower[z + row][left - 1] for row in range(2)]):
                for row in range(2):
                    tower[z + row][right] = "."
                    tower[z + row][left - 1] = "@"

    for _ in range(4):
        if "".join(tower[z + 0]) == "".join(EMPTY_LINE):
            del tower[z + 0]

    if not can_drop:
        for row in range(4):
            if row > len(tower) - 1:
                break
            for col in range(1, 8):
                if tower[z + row][col] == "@":
                    tower[z + row][col] = "#"

    print_grid(tower, SHOULD_PRINT)
    return can_drop


def print_grid(tower, SHOULD_PRINT):
    if not SHOULD_PRINT:
        return
    print()
    for row in tower[:PRINT_HEIGHT]:
        print("".join(row))


class Rock(NamedTuple):
    height: int
    width: int
    initial: list[list[str]]
    name: str


EMPTY_LINE = list("|.......|")
I_HOR_LINE = [
    list("|..@@@@.|")
]
I_CROSS = [
    list("|...@...|"),
    list("|..@@@..|"),
    list("|...@...|"),
]
I_L_SHAPE = [
    list("|....@..|"),
    list("|....@..|"),
    list("|..@@@..|"),
]
I_VER_LINE = [
    list("|..@....|"),
    list("|..@....|"),
    list("|..@....|"),
    list("|..@....|"),
]
I_SQUARE = [
    list("|..@@...|"),
    list("|..@@...|"),
]
HOR_LINE = Rock(1, 4, I_HOR_LINE, "hor_line")
CROSS    = Rock(3, 3, I_CROSS, "cross")
L_SHAPE  = Rock(3, 3, I_L_SHAPE, "l_shape")
VER_LINE = Rock(4, 1, I_VER_LINE, "ver_line")
SQUARE   = Rock(2, 2, I_SQUARE, "square")
