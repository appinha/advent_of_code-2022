from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import X, Y
from aoc_lib.imports import *

from aoc_framework.solver.timer import Timer


Location = tuple[int, int]
BeaconsBySensor = dict[Location, Location]
DistanceBySensor = dict[Location, float]

calc_md = lib.calc_manhattan_distance


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        beacons_by_sensor, distance_by_sensor = process_input(raw_input)
        row_y = 2_000_000 if not self.is_testing else 10
        no_beacons_x = find_no_beacon_locations_in_row(beacons_by_sensor, distance_by_sensor, row_y)
        return len(no_beacons_x)

    def solve_part_2(self, raw_input: str):
        beacons_by_sensor, distance_by_sensor = process_input(raw_input)
        bound = 4_000_000
        all_intersections = find_all_intersections(beacons_by_sensor, distance_by_sensor, bound)
        intersection = find_missing_intersection(beacons_by_sensor, all_intersections)
        return bound * intersection[X] + intersection[Y]


def process_input(raw_input: str):
    beacons_by_sensor: BeaconsBySensor = {}
    distance_by_sensor: DistanceBySensor = {}
    for line in raw_input:
        sensor_x, sensor_y, beacon_x, beacon_y = lib.find_all_integers(line)
        sensor, beacon = (sensor_x, sensor_y), (beacon_x, beacon_y)

        beacons_by_sensor[sensor] = beacon
        distance_by_sensor[sensor] = calc_md(sensor, beacon)

    return beacons_by_sensor, distance_by_sensor


def find_no_beacon_locations_in_row(
    beacons_by_sensor: BeaconsBySensor, distance_by_sensor: DistanceBySensor, row_y: int,
):
    no_beacons_x = set()
    for sensor, beacon in beacons_by_sensor.items():
        remaining_distance = distance_by_sensor[sensor] - abs(row_y - sensor[Y])
        if remaining_distance < 0:
            continue

        possible_no_beacons_x = [sensor[X]]
        for i in range(1, remaining_distance + 1):
            possible_no_beacons_x += [sensor[X] - i, sensor[X] + i]

        if beacon[Y] == row_y and beacon[X] in possible_no_beacons_x:
            possible_no_beacons_x.remove(beacon[X])

        no_beacons_x.update(possible_no_beacons_x)

    return no_beacons_x


def list_locations_just_outside_ranges(distance_by_sensor: DistanceBySensor, bound: int):

    def in_bounds(coord: Location):
        return all(0 < i < bound for i in coord)

    locations_1_by_sensor: dict[Location, set[Location]] = collections.defaultdict(set)
    locations_2_by_sensor: dict[Location, set[Location]] = collections.defaultdict(set)
    for sensor, distance in distance_by_sensor.items():
        border = int(distance + 1)
        north = (sensor[X], sensor[Y] - border)
        south = (sensor[X], sensor[Y] + border)
        west  = (sensor[X] - border, sensor[Y])
        east  = (sensor[X] + border, sensor[Y])
        locations = [north, east, south, west]
        locations_1_by_sensor[sensor].update(locations)
        locations_2_by_sensor[sensor].update(locations)

        s = 1
        for _ in range(north[X] + 1, east[X]):
            coord = (int(north[X] + s), int(north[Y] + s))
            if in_bounds(coord):
                locations_1_by_sensor[sensor].add(coord)
            s += 1

        s = 1
        for _ in range(west[X] + 1, south[X]):
            coord = (int(west[X] + s), int(west[Y] + s))
            if in_bounds(coord):
                locations_1_by_sensor[sensor].add(coord)
            s += 1

        x, y = -1, 1
        for _ in range(north[Y] + 1, west[Y]):
            coord = (int(north[X] + x), int(north[Y] + y))
            if in_bounds(coord):
                locations_2_by_sensor[sensor].add(coord)
            x -= 1
            y += 1

        x, y = -1, 1
        for _ in range(east[Y] + 1, south[Y]):
            coord = (int(east[X] + x), int(east[Y] + y))
            if in_bounds(coord):
                locations_2_by_sensor[sensor].add(coord)
            x -= 1
            y += 1

    return locations_1_by_sensor, locations_2_by_sensor


def find_all_intersections(
    beacons_by_sensor: BeaconsBySensor, distance_by_sensor: DistanceBySensor, bound: int,
):
    locations_1, locations_2 = \
        list_locations_just_outside_ranges(distance_by_sensor, bound)

    sensor_pairs = lib.list_combinations(beacons_by_sensor.keys(), 2)
    all_intersections: set[Location] = set()
    for sensor_a, sensor_b in sensor_pairs:
        sensors_distance = calc_md(sensor_a, sensor_b)
        if sensors_distance > distance_by_sensor[sensor_a] + distance_by_sensor[sensor_b]:
            continue

        intersections = locations_1[sensor_a].intersection(locations_2[sensor_b])
        all_intersections.update(intersections)
        intersections = locations_2[sensor_a].intersection(locations_1[sensor_b])
        all_intersections.update(intersections)

    return all_intersections


def find_missing_intersection(beacons_by_sensor: BeaconsBySensor, all_intersections: set[Location]):

    def is_outside_sensor_range(sensor: Location, beacon: Location, intersection: Location):
        return calc_md(sensor, intersection) > calc_md(sensor, beacon)

    def is_outside_all_ranges(intersection: Location):
        return all(is_outside_sensor_range(sensor, beacon, intersection)
            for sensor, beacon in beacons_by_sensor.items())

    for intersection in all_intersections:
        if is_outside_all_ranges(intersection):
            return intersection


def solve_part_2_math(raw_input: str):
        beacons_by_sensors = process_input(raw_input)
        bound = 4_000_000

        def in_bounds(coord: Location):
            return all(0 < i < bound for i in coord)

        def is_outside_sensor_range(sensor: Location, beacon: Location, intersection: Location):
            sensor_radius = calc_md(sensor, beacon)
            intersection_radius = calc_md(sensor, intersection)
            return intersection_radius > sensor_radius

        a_coeffs, b_coeffs = set(), set()
        for sensor, beacon in beacons_by_sensors.items():
            radius = calc_md(sensor, beacon)

            north = sensor[X] + sensor[Y] - (radius + 1)
            south = sensor[X] + sensor[Y] + (radius + 1)
            west  = sensor[Y] - sensor[X] - (radius + 1)
            east  = sensor[Y] - sensor[X] + (radius + 1)

            a_coeffs.update([east, west])
            b_coeffs.update([north, south])

        for a in a_coeffs:
            for b in b_coeffs:
                intersection = ((b - a) // 2, (a + b) // 2)
                if in_bounds(intersection):
                    # print()
                    if all(is_outside_sensor_range(sensor, beacon, intersection)
                        for sensor, beacon in beacons_by_sensors.items()):
                        print("a:", a, "b:", b, "intersection:", intersection)
                        return bound * intersection[X] + intersection[Y]
