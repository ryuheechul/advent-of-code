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


def expand_map(galaxy_map: list[list[str]]):
    rows, cols = detect_empty_rows(galaxy_map), detect_empty_cols(galaxy_map)

    def expand_col(row: list[str]):
        some_duplicated = (
            [col, col] if x in cols else [col] for x, col in enumerate(row)
        )
        return [item for arr in some_duplicated for item in arr]

    some_duplicated = (
        [row, row] if y in rows else [row]
        for y, row in enumerate(expand_col(r) for r in galaxy_map)
    )

    return [item for arr in some_duplicated for item in arr]


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

    expanded_map = expand_map(galaxy_map)

    galaxy_count, coords_map = get_coords(expanded_map)

    pairs = unique_perms_of_pairs(galaxy_count)

    answer = sum(distance(coords_map[a], coords_map[b]) for (a, b) in pairs)

    print(answer)
