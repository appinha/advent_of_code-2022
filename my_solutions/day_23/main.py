from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import X, Y, N, S, E, W, NW, NE, SE, SW
from aoc_lib.imports import *


PRINT_GRID = False


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        elves = process_input(raw_input)
        return simulate(elves, 10)

    def solve_part_2(self, raw_input: str):
        elves = process_input(raw_input)
        return simulate(elves, 1_000, is_part_2=True)


Location = tuple[int, int]


def process_input(raw_input: str):
    elves: dict[Location, bool] = {}
    y = 0
    for line in raw_input:
        x = 0
        for char in line:
            if char == "#":
                elves[(x, y)] = True
            x += 1
        y += 1
    return elves


NEIGHBOURS = {
    "all": [N, S, E, W, NE, NW, SE, SW],
    N: [NW, N, NE],
    S: [SW, S, SE],
    W: [NW, W, SW],
    E: [NE, E, SE],
}


def simulate(elves: dict[Location, bool], max_steps: int, is_part_2=False):
    print_grid(elves)
    directions = Deque([N, S, W, E])

    def list_neighbours(location: Location, relative_neighbours: list[Location]):
        return [lib.cross_sum(location, rel_neighbour) for rel_neighbour in relative_neighbours]

    def no_elf_in(neighbours):
        return all([n not in elves for n in neighbours])

    def is_stable(elf: Location):
        return no_elf_in(list_neighbours(elf, NEIGHBOURS["all"]))

    def move_elf(elves, src, dst):
        del elves[src]
        elves[dst] = True

    steps = 1
    while steps < max_steps + 1:
        if all([is_stable(elf) for elf in elves]):
            if is_part_2:
                return steps
            break

        proposition_by_elf = {}
        for elf in elves:
            if is_stable(elf):
                continue
            for direction in directions:
                if no_elf_in(list_neighbours(elf, NEIGHBOURS[direction])):
                    proposition_by_elf[elf] = lib.cross_sum(elf, direction)
                    break

        proposition_counts = collections.Counter(proposition_by_elf.values())
        for elf, proposition in proposition_by_elf.items():
            if proposition_counts[proposition] == 1:
                move_elf(elves, elf, proposition)

        directions.rotate(-1)
        print_grid(elves)
        steps += 1

    return count_empty(elves)


def count_empty(elves):
    (min_x, min_y), (max_x, max_y) = lib.find_limits(elves)
    count = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) not in elves:
                count += 1
    return count


def print_grid(elves):
    if not PRINT_GRID:
        return

    (min_x, min_y), (max_x, max_y) = lib.find_limits(elves)
    shape = (abs(max_x - min_x) + 1, abs(max_y - min_y) + 1)

    grid = [["." for _ in range(shape[X])] for _ in range(shape[Y])]
    for x, y in elves:
        grid[y - min_y][x - min_x] = "#"

    lib.pretty_print_grid(grid)
    print()
