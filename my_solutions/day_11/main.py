from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input: str):
        return play(
            monkeys=process_input(raw_input),
            rounds=20,
            reducer=lambda item: item // 3
        )

    def solve_part_2(self, raw_input: str):
        monkeys = process_input(raw_input)
        lcd = lib.prod([m.test for m in monkeys])
        return play(
            monkeys=monkeys,
            rounds=10_000,
            reducer=lambda item: item % lcd
        )


def process_input(raw_input: str):
    monkeys = []
    for i, block in enumerate(raw_input):
        monkey = {"n": i}
        for line in block.split("\n"):
            if "Starting items" in line:
                monkey["items"] = lib.find_all_integers(line)
            if "Operation" in line:
                expression = line.strip().replace("Operation: new = ", "").split(" ")
                monkey["expression"] = {"operator": expression.pop(1), "operands": expression}
            if "Test" in line:
                monkey["test"] = lib.find_all_integers(line)[0]
            if "If true" in line:
                monkey["if true"] = lib.find_all_integers(line)[0]
            if "If false" in line:
                monkey["if false"] = lib.find_all_integers(line)[0]
        monkeys.append(Monkey(**monkey))
    return monkeys


def play(monkeys: list[Monkey], rounds: int, reducer: Callable[[int], int]):
    for _ in range(rounds):
        for monkey in monkeys:
            actions = monkey.play_turn(reducer)
            for item, n in actions:
                monkeys[n].fetch_item(item)

    inspected = [m.inspected for m in monkeys]
    return lib.prod(heapq.nlargest(2, inspected))


class Monkey():
    def __init__(self, **kwargs):
        self.n: int = kwargs["n"]
        self.items: list[int] = kwargs["items"]
        self.operator: str = kwargs["expression"]["operator"]
        self.operands: list[str] = kwargs["expression"]["operands"]
        self.test: int = kwargs["test"]
        self.if_true: int = kwargs["if true"]
        self.if_false: int = kwargs["if false"]

        self.inspected: int = 0

    def __repr__(self):
        return f"""Monkey {self.n}:
  Starting items: {self.items}
  Operation: new = {self.operands[0]} {self.operator} {self.operands[1]}
  Test: divisible by {self.test}
    If true: throw to monkey {self.if_true}
    If false: throw to monkey {self.if_false}
  Inspected: {self.inspected}
"""

    def play_turn(self, reducer: Callable[[int], int]):
        actions: list[tuple[int, int]] = []
        for item in self.items:
            item = reducer(self.make_operation(item))
            if item % self.test == 0:
                actions.append((item, self.if_true))
            else:
                actions.append((item, self.if_false))
        self.inspected += len(self.items)
        self.items = []
        return actions

    def make_operation(self, item: int):

        def process(operand: str):
            return item if operand == "old" else int(operand)

        if self.operator == "+":
            return sum([process(o) for o in self.operands])
        if self.operator == "*":
            return lib.prod([process(o) for o in self.operands])

    def fetch_item(self, item: int):
        self.items.append(item)
