import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from pprint import pprint

from collections import defaultdict


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input):
        size_by_path = self._get_dir_sizes(raw_input)
        return sum(size for size in size_by_path.values() if size <= 100000)

    def solve_part_2(self, raw_input):
        size_by_path = self._get_dir_sizes(raw_input)
        needed_space = self._calculate_needed_space(size_by_path["/"])
        return min(size for size in size_by_path.values() if size > needed_space)

    def _get_dir_sizes(self, raw_input):
        path_stack = lib.Stack()
        contents_by_path = defaultdict(list)
        size_by_path = defaultdict(int)

        def build_curr_path():
            return "/".join(path_stack.items)

        def sum_contents_then_pop(curr_path):
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

    def _calculate_needed_space(self, used_space):
        AVAILABLE_SPACE = 70_000_000
        UPDATE_SIZE = 30_000_000
        unused_space = AVAILABLE_SPACE - used_space
        return UPDATE_SIZE - unused_space