from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import Stack
from aoc_lib.imports import *


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: str):
        dir_size_by_path = process_input(raw_input)
        return sum(size for size in dir_size_by_path.values() if size <= 100000)

    def solve_part_2(self, raw_input: str):
        dir_size_by_path = process_input(raw_input)
        needed_space = calculate_needed_space(dir_size_by_path["/"])
        return min(size for size in dir_size_by_path.values() if size > needed_space)


def process_input(raw_input: str):
    path_stack = Stack()
    contents_by_path = collections.defaultdict(list)
    size_by_path = collections.defaultdict(int)

    def build_curr_path():
        return "/".join(path_stack.items)

    def sum_contents_then_pop(curr_path: str):
        size_by_path[curr_path] = sum(content if lib.is_int(content) else size_by_path[content]
            for content in contents_by_path[curr_path])
        path_stack.pop()

    for line in raw_input:
        curr_path = build_curr_path()
        match line.strip("$").split():
            case ["cd", ".."]:
                sum_contents_then_pop(curr_path)
            case ["cd", dir_name]:
                path_stack.push(dir_name)
            case ["dir", dir_name]:
                contents_by_path[curr_path].append(curr_path + "/" + dir_name)
            case [size, _]:
                contents_by_path[curr_path].append(int(size))

    while path_stack.items:
        sum_contents_then_pop(build_curr_path())

    return size_by_path


def calculate_needed_space(used_space: int):
    AVAILABLE_SPACE = 70_000_000
    UPDATE_SIZE = 30_000_000
    unused_space = AVAILABLE_SPACE - used_space
    return UPDATE_SIZE - unused_space
