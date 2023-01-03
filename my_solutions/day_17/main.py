from __future__ import annotations
import sys; sys.path.insert(0, '..')
import aoc_lib as lib
from aoc_lib import ROW, COL
from aoc_lib.imports import *


PRINT_GRID = False


class DayPuzzleSolver():
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, raw_input: str):
        jets = process_input(raw_input)
        return play_tetris(jets, 2022)

    def solve_part_2(self, raw_input: str):
        jets = process_input(raw_input)
        return play_tetris(jets, 1_000_000_000_000)


Location = tuple[int, int]
Rock = list[Location]


HOR_LINE = [(0, 0), (0, 1), (0, 2), (0, 3)]
CROSS    = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
L_SHAPE  = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
VER_LINE = [(0, 0), (1, 0), (2, 0), (3, 0)]
SQUARE   = [(0, 0), (0, 1), (1, 0), (1, 1)]


class Cycle(NamedTuple):
    top: int
    diff: int


def process_input(raw_input: str):
    return lib.cycle(list(raw_input))


def play_tetris(jets: Iterable[str], max_rocks: int):
    rocks = lib.cycle([HOR_LINE, CROSS, L_SHAPE, VER_LINE, SQUARE])
    filled = set([(0, col) for col in range(7)])  # initialized with floor
    rock_count = 0
    top = 0

    tracker = collections.defaultdict(list)
    target = -1

    def get_rock_initial_coords(rock: Rock):
        return [lib.cross_sum(coord, (top + 4, 2)) for coord in rock]

    def drop_rock(top: int):
        can_drop = True
        while can_drop:
            jet = next(jets)
            move_rock(filled, rock, jet)  # move sideways
            can_drop = move_rock(filled, rock, "v")  # move down (drop)

        filled.update(rock)
        return max([top, find_top_row(rock)])

    def calculate_final_top():
        remaining = top - ((rock_count // cycle_rock_count) * cycle_height)
        return remaining + ((max_rocks // cycle_rock_count) * cycle_height)

    def find_target():
        if rock_count != 0 and rock_count % 5 == 0:
            tracker[rock_count] = [Cycle(top, 0)]

        potential_cycle_rock_counts = [rc for rc in tracker if rock_count % rc == 0]
        for rc in potential_cycle_rock_counts:
            last_top = tracker[rc][-1].top
            if last_top != top:
                tracker[rc].append(Cycle(top, top - last_top))

            if len(tracker[rc]) > 3 and \
                tracker[rc][1].diff == tracker[rc][2].diff == tracker[rc][3].diff:
                cycle_rock_count = rc
                cycle_height = tracker[rc][-1].diff
                target = rock_count + (max_rocks % cycle_rock_count)
                return cycle_rock_count, cycle_height, target

            elif len(tracker[rc]) > 3 and tracker[rc][-1].diff != tracker[rc][-2].diff:
                del tracker[rc]

        return None, None, -1

    while True:
        rock = get_rock_initial_coords(next(rocks))
        top = drop_rock(top)
        rock_count += 1

        # part 1
        if rock_count == max_rocks:
            return top

        # part 2
        if rock_count == target:
            return calculate_final_top()

        if target > 0:
            continue
        cycle_rock_count, cycle_height, target = find_target()


def find_top_row(coords: Location):
    return max([row for row, _ in coords])


def move_rock(filled: set[Location], rock: Rock, direction: str):
    if PRINT_GRID:
        print("\ndirection:", direction)

    def check(coords: Location):
        return all([0 <= col < 7 and (row, col) not in filled for row, col in coords])

    can_drop = True
    if direction == "v":
        new_coords = [lib.cross_sum(coord, (-1, 0)) for coord in rock]
        if check(new_coords):
            del rock[:]
            rock.extend(new_coords)
        else:
            can_drop = False

    elif direction == ">":
        new_coords = [lib.cross_sum(coord, (0, 1)) for coord in rock]
        if check(new_coords):
            del rock[:]
            rock.extend(new_coords)

    elif direction == "<":
        new_coords = [lib.cross_sum(coord, (0, -1)) for coord in rock]
        if check(new_coords):
            del rock[:]
            rock.extend(new_coords)

    print_grid(filled, rock, find_top_row(rock), PRINT_GRID)
    return can_drop


def print_grid(filled: set[Location], current_rock: Rock, top: int, PRINT_GRID: bool):
    if not PRINT_GRID:
        return

    tower = [list(".......") for _ in range(top + 1)]

    for row, col in current_rock:
        tower[row][col] = "@"
    for row, col in filled:
        if row != 0:
            tower[row][col] = "#"

    print()
    for row in reversed(tower[1:]):
        print("|" + "".join(row) + "|")
    print("+-------+")
