from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import X, Y, ROW, COL, Grid
from aoc_lib.imports import *


PRINT_GRID = False


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str):
        cave, height = process_input(raw_input)

        simulate(cave, height)
        print_cave(cave)

        return len(numpy.where(cave.grid == "o")[0])

    def solve_part_2(self, raw_input: str):
        cave, height = process_input(raw_input, has_floor=True)
        insert_floor_rocks(cave, height)

        simulate(cave, height)
        print_cave(cave)

        return len(numpy.where(cave.grid == "o")[0])


def process_input(raw_input: str, has_floor=False):

    def get_height():
        all_coords = lib.find_all_coords(raw_input.replace("->", ""))
        _, rows = zip(*all_coords)
        return max(rows) + 1 + (2 if has_floor else 0)

    def get_shape():
        return (get_height(), 1_000)

    shape = get_shape()
    cave = Grid(shape=shape, fill_value=".")

    cave[0, 500] = "+"  # insert sand provider
    insert_rocks(raw_input, cave)

    return cave, shape[ROW] - 1


def insert_rocks(raw_input: str, cave: Grid):

    def draw_line(start, end):
        i = X if start[X] != end[X] else Y
        get_location = lambda j: (end[Y], j) if i == X else (j, end[X])
        start_i, end_i = sorted([start[i], end[i]])
        for j in range(start_i, end_i + 1):
            cave[get_location(j)] = "#"

    for line in raw_input.split("\n"):
        coords = lib.find_all_coords(line.replace("->", ""))
        for i in range(1, len(coords)):
            draw_line(start=coords[i - 1], end=coords[i])


def insert_floor_rocks(cave, floor):
    for col in range(cave.shape[COL]):
        cave[floor, col] = "#"


def find_cave_limits(cave, limiter):
    rocks = [(row, col)
        for (row, col), value in cave.value_by_location.items()
        if value == limiter]
    rows, cols = zip(*rocks)
    return {"left": min(cols), "right": max(cols), "bottom": max(rows)}


def simulate(cave, height):

    def check(location):
        return cave.has_location((location)) and cave[location] != "#" and cave[location] != "o"

    def drop_sand():
        col = 500
        for row in range(height):
            if check((row + 1, col)):  # down
                pass
            elif check((row + 1, col - 1)):  # diagonal left
                col -= 1
            elif check((row + 1, col + 1)):  # diagonal right
                col += 1
            else:
                cave[row, col] = "o"
                return (col, row) != (500, 0)
        return False

    while drop_sand():
        pass


def print_cave(cave):
    if not PRINT_GRID:
        return
    limits = find_cave_limits(cave, "o")
    for row in range(limits["bottom"] + 2):
        line = ""
        for col in range(limits["left"] - 1, limits["right"] + 2):
            if cave.has_location((row, col)):
                line += cave[row, col]
        print(line)
