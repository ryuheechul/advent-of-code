# https://adventofcode.com/2024/day/12

# find part 1 at ./part1.py
# find part 2 at ./part2.py

from typing import Iterable


filename = ["sample1.txt", "sample2.txt", "sample3.txt", "input.txt"][3]

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


# 8 fence walls surroinding a plot (being (0,0))
surround_template = [
    (-1, -1),  # phantom fence that helps join real fences
    (0, -1),
    (1, -1),  # phantom fence that helps join real fences
    (-1, 0),
    (1, 0),
    (-1, 1),  # phantom fence that helps join real fences
    (0, 1),
    (1, 1),  # phantom fence that helps join real fences
]


# assuming x and y both are bigger than 1 for convenience
def fences_of_plot(coords: Coords):
    x, y = coords

    return [(sx + x, sy + y) for sx, sy in surround_template]


def fences_of_group(group: Iterable[Coords]):
    # first combine all fences of each plot and exclude the plots themselves
    # this will give this shape

    return list(
        set(c for coords in group for c in fences_of_plot(coords) if c not in group)
    )
    # the above will return the coords of '+' which helps to chain the fences
    # +++++++
    # +OOOOO+           +++
    # +O+O+O+           +C++            000        0000        0000
    # +OOOOO+     or    +CC+     or     0+0   or   0++0   or   0++0
    # +O+O+O+           ++C+            000        0000        00+0
    # +OOOOO+            +++                                   0000
    # +++++++
    #
    # whether it's inside or outside, we can count how many plot that one fence is touching;
    # for the calculation look at `true_fence_count` function


def true_fence_count(fence: Coords, plots: set[Coords]):
    touch_point = 0

    neighbors = potential_neighbors_for_a_coords(fence)
    for neighbor in neighbors:
        if neighbor in plots:
            touch_point += 1

    return touch_point


def score_fence(fence: Coords, plots: set[Coords]):
    area = len(plots)
    return area * true_fence_count(fence, plots)


def score_fences(group: set[Coords]):
    fences = fences_of_group(group)

    group_dict = sort_to_groups([(coords, "+") for coords in fences])

    fences_set = group_dict["+"]

    def _score_fences(fs: Iterable[Coords]):
        return sum(score_fence(fence, group) for fence in fs)

    return sum(_score_fences(fences) for fences in fences_set)


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


with open(filename, "r") as reader:
    plots = [[plot for plot in line.strip()] for line in reader.readlines()]

    group_dict = sort_to_groups(list(grid_iterator(plots)))

    s = sum(score_fences(group) for groups in group_dict.values() for group in groups)

    print(s)
