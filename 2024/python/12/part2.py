# https://adventofcode.com/2024/day/12

# find part 1 at ./part1.py
# find part 2 at ./part2.py

from typing import Iterable


filename = [
    "sample1.txt",
    "sample2.txt",
    "sample3.txt",
    "sample4.txt",
    "sample5.txt",
    "input.txt",
][5]

Coords = tuple[int, int]


def potential_neighbors_for_a_coords(coords: Coords):
    x, y = coords

    north = x, y - 1
    east = x + 1, y
    south = x, y + 1
    west = x - 1, y

    # tolerating the slight efficiency of being out side of the size of the grid
    return [(x, y) for x, y in [north, east, south, west] if x >= 0 and y >= 0]


def potential_neighbors_for_a_group(group: Iterable[Coords]):
    return [
        each_coord
        for coord in group
        for each_coord in potential_neighbors_for_a_coords(coord)
    ]


def find_all(plot: str, current: Coords, coords_set: list[tuple[Coords, str]]):
    same_plot_only = [c for c, p in coords_set if p == plot]

    result = {current}
    plots_to_search = {current}

    while len(plots_to_search):
        to_search = plots_to_search.pop()

        for neighbor in potential_neighbors_for_a_coords(to_search):
            if neighbor in result:
                continue

            if neighbor in same_plot_only:
                result.add(neighbor)
                plots_to_search.add(neighbor)

    return result


def sort_to_groups(coords_set: list[tuple[Coords, str]]):
    group_dict: dict[str, list[set[Coords]]] = dict()

    for (x, y), plot in coords_set:
        coords = (x, y)
        groups = group_dict.get(plot)
        if groups:
            belong_to_any_existing_group = False
            if len(groups):
                for group in groups:
                    if coords in potential_neighbors_for_a_group(group):
                        group.add((coords))
                        belong_to_any_existing_group = True

            # including groups being empty for some reason
            if not belong_to_any_existing_group:
                # groups.append({coords}) # this will lead to broken pieces for the ones that are not immediately touching the existing group at the time of traversing
                # hence it's important to add everything at once and the rest of traverse would be just "checking the math"
                groups.append(find_all(plot, coords, coords_set))

        else:
            # group_dict[plot] = [{coords}] # <- is wrong for the same reason above
            group_dict[plot] = [find_all(plot, coords, coords_set)]

    return group_dict


def grid_iterator(plots: list[list[str]]):
    for y, line in enumerate(plots):
        for x, plot in enumerate(line):
            # add 2 more so not only adding a fence around it is easier but also doing the math
            yield (x + 2, y + 2), plot


# horizontal lines
def count_straight_lines(target: list[int], upper: list[int], lower: list[int]):
    count = 0

    last_with_upper = False
    last_with_lower = False

    for x, plot_target in enumerate(target):
        p_upper = upper[x]
        p_lower = lower[x]

        if plot_target:
            # either 1s itself discontinued or 0s above
            if not p_upper and not last_with_upper:
                count += 1

            # either 1s itself discontinued or 0s below
            if not p_lower and not last_with_lower:
                count += 1

        last_with_upper = plot_target and not p_upper
        last_with_lower = plot_target and not p_lower

    return count


# horizontal scan
def scan(grid: list[list[int]]):
    range_to_target_inner_grid = (i + 1 for i in range(len(grid) - 2))

    def count(i: int):
        upper, current, lower = grid[i - 1], grid[i], grid[i + 1]

        return count_straight_lines(current, upper, lower)

    return sum(count(i) for i in range_to_target_inner_grid)


# flip to reuse horizontal calculations instead of writing more functions for vertical calculations
def flip(grid: list[list[int]]):
    new_grid = [[0 for _ in range(len(grid))] for _ in range(len(grid[0]))]
    for y, line in enumerate(grid):
        for x, e in enumerate(line):
            new_grid[x][y] = e

    return new_grid


def count_with_grid(group: set[Coords]):
    # sort of like a clean test bed
    def gen_grid():
        bx, by = 0, 0

        for x, y in group:
            if x > bx:
                bx = x
            if y > by:
                by = y

        grid = [[0 for _ in range(bx + 1)] for _ in range(by + 1)]

        for x, y in group:
            grid[y - 1][x - 1] = 1
        return grid

    grid = gen_grid()
    flipped = flip(grid)  # flip to reuse horizontal calculations

    return scan(grid) + scan(flipped)


def score_sides(group: set[Coords]):
    area = len(group)
    count = count_with_grid(group)

    return area * count


with open(filename, "r") as reader:
    plots = [[plot for plot in line.strip()] for line in reader.readlines()]

    group_dict = sort_to_groups(list(grid_iterator(plots)))

    s = sum(score_sides(group) for groups in group_dict.values() for group in groups)

    print(s)
