from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        number_by_monkey, expression_by_monkey = process_input(raw_input)
        return do_monkey_math(number_by_monkey, expression_by_monkey)

    def solve_part_2(self, raw_input: str):
        number_by_monkey, expression_by_monkey = process_input(raw_input)
        number_by_monkey["humn"] = "Amanda"
        return do_monkey_math(number_by_monkey, expression_by_monkey, is_part_2=True)


def process_input(raw_input: str):
    number_by_monkey: dict[str, int] = {}
    expression_by_monkey: dict[str, list] = {}

    for line in raw_input:
        words = line.replace(":", "").split(" ")
        if len(words) == 2:
            number_by_monkey[words[0]] = int(words[1])
        else:
            expression_by_monkey[words[0]] = words[1:]

    return number_by_monkey, expression_by_monkey


def do_monkey_math(
    number_by_monkey: dict[str, int], expression_by_monkey: dict[str, list], is_part_2=False
):

    def substitute_in_expression(expression: list):
        new_expression = copy.deepcopy(expression)
        for i in [0, 2]:
            if expression[i] in number_by_monkey:
                new_expression[i] = number_by_monkey[expression[i]]
        return new_expression

    def eval_expression(expression: list):
        if all(map(lib.is_number, [expression[0], expression[2]])):
            number_by_monkey[monkey] = calc_expression(expression)
        else:
            new_expression_by_monkey[monkey] = expression

    while expression_by_monkey:
        new_expression_by_monkey = {}
        for monkey, expression in expression_by_monkey.items():
            eval_expression(substitute_in_expression(expression))
        if is_part_2 and any(map(lib.is_number, expression_by_monkey["root"])):
            return find_my_number(expression_by_monkey)
        expression_by_monkey = new_expression_by_monkey

    return number_by_monkey["root"]


def find_my_number(expression_by_monkey: dict[str, list]):

    def find_number_and_monkey(expression: list):
        return (expression[0], expression[2]) if lib.is_number(expression[0]) \
            else (expression[2], expression[0])

    result, monkey = find_number_and_monkey(expression_by_monkey["root"])
    while True:
        expression = expression_by_monkey[monkey]
        number, monkey = find_number_and_monkey(expression)
        result = update_result(expression, number, result)
        if monkey == "Amanda":
            return result


def update_result(expression: dict[str, list], number: int, result: int):
    operation = expression[1]
    if operation == "+":
        return calc_expression([result, "-", number])
    if operation == "-" and expression[0] == number:
        return calc_expression([-result, "+", number])
    if operation == "-":
        return calc_expression([result, "+", number])
    if operation == "*":
        return calc_expression([result, "/", number])
    if operation == "/":
        return calc_expression([result, "*", number])


def calc_expression(expression: list):
    if expression[1] == "+":
        return expression[0] + expression[2]
    if expression[1] == "-":
        return expression[0] - expression[2]
    if expression[1] == "*":
        return expression[0] * expression[2]
    if expression[1] == "/":
        return expression[0] // expression[2]
