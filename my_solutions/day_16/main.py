from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


Valve = str
ValvePair = tuple[Valve, Valve]


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        distances, flow_rates = process_input(raw_input)
        return find_the_most_pressure_released(distances, flow_rates, 30)

    def solve_part_2(self, raw_input: str):
        distances, flow_rates = process_input(raw_input)
        return find_the_most_pressure_released(distances, flow_rates, 26, elephant_help=True)


def process_input(raw_input: str):
    valves: set[Valve] = set()
    distances: dict[ValvePair, int] = collections.defaultdict(lambda: 100)
    flow_rates: dict[Valve, int] = dict()

    for line in raw_input:
        result = re.search(r'Valve ([A-Z]+).+rate=(\d+);.+valves? ([A-Z ,]+)', line)
        valve, flow_rate, connected_valves = result.groups()
        valves.add(valve)
        if flow_rate != "0":
            flow_rates[valve] = int(flow_rate)
        for connected_valve in connected_valves.split(", "):
            distances[valve, connected_valve] = 1

    # floyd-warshall
    for a, b, c in itertools.product(valves, valves, valves):
        distances[b, c] = min(distances[b, c], distances[b, a] + distances[a, c])

    return distances, flow_rates


def find_the_most_pressure_released(
    distances: dict[ValvePair, int], flow_rates: dict[Valve, int], minutes: int, elephant_help=False
):

    @functools.cache
    def search(time: int, src='AA', all_dsts=frozenset(flow_rates), elephant_help=False):
        remaining_time = lambda dst: time - distances[src, dst] - 1

        def calc_total_pressure_released(dst: Valve):
            time = remaining_time(dst)
            return flow_rates[dst] * time + search(time, dst, all_dsts - {dst}, elephant_help)

        return max([
            calc_total_pressure_released(dst)
            for dst in all_dsts
            if distances[src,dst] < time
        ] + [0 if not elephant_help else search(26, all_dsts=all_dsts)])

    return search(minutes, elephant_help=elephant_help)
