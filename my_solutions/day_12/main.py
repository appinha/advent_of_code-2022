from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import Coord2D, a_star, manhattan_distance, node_to_path
from aoc_lib.imports import *

from string import ascii_lowercase


PRINT_GRID = False


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        heightmap, locations = process_input(raw_input)

        maze = Maze(heightmap, locations["start"], locations["goal"])
        path = find_path(maze)
        maze.mark(path)
        print_maze(maze)

        return len(path) - 1

    def solve_part_2(self, raw_input: str):
        heightmap, locations = process_input(raw_input, all_possible_starts=True)

        path_lengths = []
        for start in locations["all_possible_starts"]:
            path = find_path(Maze(heightmap, start, locations["goal"]))
            if path is not None:
                path_lengths.append(len(path) - 1)

        return min(path_lengths)


def process_input(raw_input: str, all_possible_starts=False):
    locations = {}
    if all_possible_starts:
        locations["all_possible_starts"] = []

    def process(char: str, row: int, col: int):
        if all_possible_starts and char in ["a", "S"]:
            locations["all_possible_starts"].append(Coord2D(row, col))
            return "a"
        if char == "S":
            locations["start"] = Coord2D(row, col)
            return "a"
        if char == "E":
            locations["goal"] = Coord2D(row, col)
            return "z"
        return char

    heightmap = [[process(char, row, col) for col, char in enumerate(line)]
        for row, line in enumerate(raw_input)]
    return heightmap, locations


class Maze(lib.Maze):
    def __init__(self, grid: list[list[str]], start: Coord2D, goal: Coord2D):
        super().__init__(grid, start, goal)

    def _successor_is_viable(self, current: Coord2D, successor: Coord2D):
        current = self.grid[current.row][current.col]
        successor = self.grid[successor.row][successor.col]
        if successor > current:
            return list(ascii_lowercase).index(successor) - list(ascii_lowercase).index(current) == 1
        return True


def find_path(maze: Maze):
    solution = a_star(
        start=maze.start,
        test_goal=maze.test_goal,
        list_successors=maze.list_successors,
        heuristic=manhattan_distance(maze.goal),
    )
    if solution is not None:
        return node_to_path(solution)


def print_maze(maze: Maze):
    if not PRINT_GRID:
        return
    print(maze)
