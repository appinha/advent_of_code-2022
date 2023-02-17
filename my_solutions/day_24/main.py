from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL, Coord2D, HashmapGrid, Queue, node_to_path
from aoc_lib.imports import *


PRINT_GRID = False


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str):
        valley_map = process_input(raw_input)
        path = find_path(valley_map)
        print_path(path, valley_map)
        return path[-1].time

    def solve_part_2(self, raw_input: str):
        valley_map = process_input(raw_input)
        path_1 = find_path(valley_map)

        valley_map.start, valley_map.goal = valley_map.goal, valley_map.start
        path_2 = find_path(valley_map, path_1[-1].time)

        valley_map.start, valley_map.goal = valley_map.goal, valley_map.start
        path_3 = find_path(valley_map, path_2[-1].time)

        print("path 1 time:", path_1[-1].time)
        print("path 2 time:", path_2[-1].time - path_1[-1].time)
        print("path 3 time:", path_3[-1].time - path_2[-1].time)

        return path_3[-1].time


def process_input(raw_input: str):
    return Map(string=raw_input)


DIFF_BY_DIRECTION = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


class Map(HashmapGrid):
    def __init__(self, string: str, dtype=str, split_func=lambda row: list(row)) -> None:
        super().__init__(string, dtype, split_func)
        self.start = Coord2D(0, 1)
        self.goal = Coord2D(self.shape[ROW] - 1, self.shape[COL] - 2)
        self.map_by_time = {0: copy.deepcopy(self._redefine_map())}

    def _redefine_map(self):
        blizzards_by_location = collections.defaultdict(list)
        for location, value in self.map.items():
            blizzards_by_location[location].append(value)
        return blizzards_by_location

    def _update_blizzard(self, curr_map):

        def get_empty_map():
            new_map = collections.defaultdict(list)
            for location, values in curr_map.items():
                if values == ["#"]:
                    new_map[location] = values
                else:
                    new_map[location].append(".")
            return new_map

        new_map = get_empty_map()

        def wrap(map, location, direction):
            curr_row, curr_col = location
            dim = ROW if direction in ["^", "v"] else COL
            limit = min if direction in ["v", ">"] else max

            get_location = lambda i: (i, curr_col) if direction in ["^", "v"] else (curr_row, i)

            next_i = limit([i for i in range(self.shape[dim]) if map[get_location(i)] != ["#"]])

            return get_location(next_i)

        def insert_into_next_location(location, value):
            next_location = lib.cross_sum(location, DIFF_BY_DIRECTION[value])
            if new_map.get(next_location) == ["#"]:
                next_location = wrap(new_map, location, value)
            if new_map.get(next_location) and "." in new_map[next_location]:
                new_map[next_location].remove(".")
            new_map[next_location].append(value)

        for location, values in curr_map.items():
            if values not in [["."], ["#"]]:
                for value in values:
                    insert_into_next_location(location, value)
        return new_map

    def update_map(self, time):
        if time not in self.map_by_time:
            self.map_by_time[time] = self._update_blizzard(self.map_by_time[time - 1])
        self.map = self.map_by_time[time]

    def _successor_is_viable(self, successor: tuple[int, int]):
        return self.map[successor] == ["."]

    def list_successors(self, location: Coord2D, time: int):
        self.update_map(time)

        successors = [Coord2D(*neighbour)
            for neighbour in self.list_neighbours(location)
            if self._successor_is_viable(neighbour)]

        if self._successor_is_viable(location):
            successors.append(location)

        return self.map, successors

    def test_goal(self, location: Coord2D) -> bool:
        return (location.row, location.col) == (self.goal.row, self.goal.col)


def find_path(valley_map: Map, initial_time=0):
    node = bfs(
        start=valley_map.start,
        initial_time=initial_time,
        initial_map=valley_map.map,
        test_goal=valley_map.test_goal,
        list_successors=valley_map.list_successors,
    )
    if node is not None:
        return node_to_path(node)


def print_path(path, valley_map):
    if not PRINT_GRID:
        return

    for step in path:
        time, state, map = step
        hashmap = {location: values[0] if len(values) == 1 else len(values)
            for location, values in map.items()}
        hashmap[state] = "E"
        print(f"time: {time}, current location: {(state.row, state.col)}")
        lib.pretty_print_hashmap_grid(hashmap, valley_map.shape)


class State(NamedTuple):
    time: int
    location: Coord2D
    map: Map


class Node():
    def __init__(self, state: State, parent: Optional[Node]):
        self.state = state
        self.parent = parent


def bfs(
    start: T,
    initial_time: int,
    initial_map: dict,
    test_goal: Callable[[T], bool],
    list_successors: Callable[[T], list[T]],
):
    initial_state = State(initial_time, start, copy.deepcopy(initial_map))
    queue = Queue()
    queue.push(Node(initial_state, None))
    visited = {(initial_time, start)}

    # keep going while there is more to explore
    while not queue.empty:
        current_node = queue.pop()
        time, location, _ = current_node.state

        if test_goal(location):
            return current_node

        time += 1

        # check where we can go next and haven't visited
        updated_map, successors =  list_successors(location, time)
        for successor in successors:
            if (time, successor) in visited:
                continue
            visited.add((time, successor))
            new_state = State(time, successor, updated_map)
            queue.push(Node(new_state, current_node))

    return None  # went through everything and never found goal
