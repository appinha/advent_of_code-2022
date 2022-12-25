import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

from typing import NamedTuple


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input):
        stacks, moves = process_input(raw_input)

        for move in moves:
            for _ in range(move.n):
                stacks[move.end - 1].push(stacks[move.start - 1].pop())

        return list_last_items(stacks)

    def solve_part_2(self, raw_input):
        stacks, moves = process_input(raw_input)

        for move in moves:
            items = [stacks[move.start - 1].pop() for _ in range(move.n)]
            for item in reversed(items):
                stacks[move.end - 1].push(item)

        return list_last_items(stacks)


def process_input(raw_input):
    return get_stacks(raw_input[0]), get_moves(raw_input[1])


def get_stacks(raw_stacks):

    def init_stacks(raw_stacks):
        columns = lib.find_all_integers(raw_stacks[0])
        return [lib.Stack() for _ in columns]

    def get_letters(raw_stack):
        return [letter for i, letter in enumerate(raw_stack) if i % 4 == 1]

    raw_stacks = list(reversed(raw_stacks.split("\n")))
    stacks = init_stacks(raw_stacks)

    for raw_stack in raw_stacks[1:]:
        for i, letter in enumerate(get_letters(raw_stack)):
            if letter != " ":
                stacks[i].push(letter)
    return stacks


class Move(NamedTuple):
    n: int
    start: int
    end: int


def get_moves(raw_moves):
    return [Move(*lib.find_all_integers(m)) for m in raw_moves.split("\n")]


def list_last_items(stacks):
    return "".join([stack.items[-1] for stack in stacks])
