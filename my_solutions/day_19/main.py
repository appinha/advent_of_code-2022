from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        blueprints = process_input(raw_input)
        return sum(blueprint.id * find_max_output(blueprint, 24, prune_cap=200)
            for blueprint in blueprints)

    def solve_part_2(self, raw_input: str):
        blueprints = process_input(raw_input)
        return math.prod(find_max_output(blueprint, 32, prune_cap=2_000)
            for blueprint in blueprints[:3])


GEO, OBS, CLA, ORE = range(4)


class Bot(NamedTuple):
    cost: numpy.array
    production: numpy.array


class State(NamedTuple):
    bot_quantity: numpy.array
    materials: numpy.array


class Blueprint():
    def __init__(
        self, id: int, ore_bot: Bot, clay_bot: Bot, obsidian_bot: Bot, geode_bot: Bot, no_bot: Bot
    ):
        self.id = id
        self.bots = [geode_bot, obsidian_bot, clay_bot, ore_bot, no_bot]

    def __repr__(self):
        return f"""
Blueprint {self.id}:
  Each ore robot costs {self.bots[ORE].cost[ORE]} ore.
  Each clay robot costs {self.bots[CLA].cost[ORE]} ore.
  Each obsidian robot costs {self.bots[OBS].cost[ORE]} ore and {self.bots[OBS].cost[CLA]} clay.
  Each geode robot costs {self.bots[GEO].cost[ORE]} ore and {self.bots[GEO].cost[OBS]} obsidian.
"""


def NP(geode=0, obsidian=0, clay=0, ore=0):
    return numpy.array([geode, obsidian, clay, ore])


def process_input(raw_input: str):
    blueprints = []
    for line in raw_input:
        id_, a, b, c, d, e, f = lib.find_all_integers(line)
        blueprint = Blueprint(
            id_,
            Bot(production=NP(ore=1), cost=NP(ore=a)),
            Bot(production=NP(clay=1), cost=NP(ore=b)),
            Bot(production=NP(obsidian=1), cost=NP(ore=c, clay=d)),
            Bot(production=NP(geode=1), cost=NP(ore=e, obsidian=f)),
            Bot(production=NP(), cost=NP()),  # for when there's not enough material to build bots
        )
        blueprints.append(blueprint)
    return blueprints


def find_max_output(blueprint: Blueprint, minutes: int, prune_cap: int):

    def sorting_key(state: State):
        return tuple(state.materials + state.bot_quantity) + tuple(state.bot_quantity)

    def prune_queue(queue: list[State]):
        return sorted(queue, key=sorting_key, reverse=True)[:prune_cap]

    queue = [State(bot_quantity=NP(ore=1), materials=NP())]

    for _ in range(minutes, 0, -1):
        new_queue = []
        for state in queue:
            for bot in blueprint.bots:
                if all(bot.cost <= state.materials):  # can afford bot
                    new_bot_quantity = state.bot_quantity + bot.production
                    new_materials = state.materials + state.bot_quantity - bot.cost
                    new_queue.append(State(new_bot_quantity, new_materials))
        queue = prune_queue(new_queue)
    return max(state.materials[GEO] for state in queue)
