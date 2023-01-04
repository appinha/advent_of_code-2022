from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import X, Y, Z
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        lava_cubes = process_input(raw_input)
        total = 0
        for cube in lava_cubes:
            covered_sides = sum(1 for neighbour in list_neighbours(cube) if neighbour in lava_cubes)
            total += 6 - covered_sides
        return total

    def solve_part_2(self, raw_input: str):
        lava_cubes = process_input(raw_input)
        limits = find_limits(lava_cubes)
        air_cubes = list_air_cubes(lava_cubes, limits)
        outer_air_cubes = find_outer_air_cubes(air_cubes, limits)
        inner_air_cubes = set(air_cubes) - set(outer_air_cubes)
        return count_sides(lava_cubes + list(inner_air_cubes))


Location = tuple[int, int, int]
Limits = tuple[int, int, int, int, int, int]


RELATIVE_NEIGHBOURS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def process_input(raw_input: str) -> list[Location]:
    return [tuple(lib.find_all_integers(line)) for line in raw_input]


def list_neighbours(coord: Location):
    return [lib.cross_sum(rel_coord, coord) for rel_coord in RELATIVE_NEIGHBOURS]


def find_limits(lava_cubes: list[Location]):
    mins, maxs = lib.find_limits(lava_cubes)
    return *mins, *maxs


def list_air_cubes(lava_cubes: list[Location], limits: Limits):
    min_x, min_y, min_z, max_x, max_y, max_z = limits
    air_cubes: list[Location] = []
    for x in range(min_x, max_x + 1):
        for y in range (min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in lava_cubes:
                    air_cubes.append((x, y, z))
    return air_cubes


def find_outer_air_cubes(air_cubes: list[Location], limits: Limits):
    min_x, min_y, min_z, max_x, max_y, max_z = limits
    outer_air_cubes = [
        cube
        for cube in air_cubes
        if cube[X] in [min_x, max_x] or cube[Y] in [min_y, max_y] or cube[Z] in [min_z, max_z]
    ]

    def is_in_distance(cube: Location, distance: int):
        return cube[X] == max_x - distance or cube[X] == min_x + distance or \
            cube[Y] == max_y - distance or cube[Y] == min_y + distance or \
            cube[Z] == max_z - distance or cube[Z] == min_z + distance

    # from outer to inner
    for distance in range(1, (max(max_x, max_y, max_z) // 2) + 1):
        count = 0
        for air_cube in air_cubes:
            if air_cube in outer_air_cubes:
                continue
            if is_in_distance(air_cube, distance):
                for neighbour in list_neighbours(air_cube):
                    if neighbour in air_cubes and neighbour in outer_air_cubes:
                        outer_air_cubes.append(air_cube)
                        count += 1
        if count == 0:
            break

    return outer_air_cubes


def count_sides(lava_cubes: list[Location]):

    def calc_distance(cube_1: Location, cube_2: Location):
        return abs(cube_1[X] - cube_2[X]) + abs(cube_1[Y] - cube_2[Y]) + abs(cube_1[Z] - cube_2[Z])

    def are_neighbours(cube_1: Location, cube_2: Location):
        return calc_distance(cube_1, cube_2) == 1

    counts = {cube: 6 for cube in lava_cubes}
    cube_pairs = lib.list_combinations(lava_cubes, 2)
    for cube_1, cube_2 in cube_pairs:
        if are_neighbours(cube_1, cube_2):
            counts[cube_1] -= 1
            counts[cube_2] -= 1
            if counts[cube_2] == 0:
                del counts[cube_2]
            if counts[cube_1] == 0:
                del counts[cube_1]

    return sum([value for value in counts.values()])
