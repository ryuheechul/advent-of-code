# https://adventofcode.com/2023/day/11

from typing import Iterable


def parse(lines: Iterable[str]):
    return [[c for c in l.strip()] for l in lines]


def detect_empty_rows(galaxy_map: list[list[str]]):
    row_length = len(galaxy_map[0])

    empty_rows = [
        idx for idx, row in enumerate(galaxy_map) if row.count(".") == row_length
    ]

    return empty_rows


def detect_empty_cols(galaxy_map: list[list[str]]):
    first_row = galaxy_map[0]

    def check_col_across_rows(idx: int):
        return all(row[idx] == "." for row in galaxy_map)

    empty_cols = [idx for idx, _ in enumerate(first_row) if check_col_across_rows(idx)]

    return empty_cols


def expand_calculator(galaxy_map: list[list[str]]):
    rows, cols = detect_empty_rows(galaxy_map), detect_empty_cols(galaxy_map)

    def compensate(coords: tuple[int, int]):
        x, y = coords

        expansion_rate = 1000_000
        # use below to debug
        # expansion_rate = 100
        # expansion_rate = 10
        # expansion_rate = 2 # this is the part 1

        # e.g. empty cols: [3, 6]
        # x: 0 1 2 3    4       5       6       7    ...
        # -:---------------------------------------------
        #  : 0 1 2   1000003 1000004         2000005 ...

        # `- 1` because the empty space itself already has 1 space
        expansion_compensation = expansion_rate - 1
        # as you see from the above (in cast part 1), when you duplicate the although the rate is 2,
        # you don't add 2 space, just 1 since 1 was already there

        x_prime = len([col for col in cols if x > col]) * expansion_compensation + x
        y_prime = len([row for row in rows if y > row]) * expansion_compensation + y

        return (x_prime, y_prime)

    return compensate


def get_coords(galaxy_map: list[list[str]]):
    count = 0
    coords_map: dict[int, tuple[int, int]] = {}
    for y, row in enumerate(galaxy_map):
        for x, col in enumerate(row):
            if col == "#":
                count += 1
                coords_map[count] = (x, y)

    return count, coords_map


def unique_perms_of_pairs(n: int):
    import itertools

    st = set(frozenset(tp) for tp in itertools.permutations(range(1, n + 1), 2))
    return [tuple(s) for s in st]


def distance(a: tuple[int, int], b: tuple[int, int]):
    ax, ay = a
    bx, by = b

    return abs(ax - bx) + abs(ay - by)


with open("input.txt", "r") as reader:
    galaxy_map = parse(reader.readlines())

    compensate = expand_calculator(galaxy_map)

    galaxy_count, coords_map = get_coords(galaxy_map)

    pairs = unique_perms_of_pairs(galaxy_count)

    answer = sum(
        distance(*[compensate(coords_map[n]) for n in (a, b)]) for (a, b) in pairs
    )

    print(answer)
