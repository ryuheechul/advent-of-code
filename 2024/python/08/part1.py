# https://adventofcode.com/2024/day/8

import itertools

Coords = tuple[int, int]


def locate_antinode(source: Coords, target: Coords):
    sx, sy = source
    mx, my = target

    ax = (mx - sx) + mx
    ay = (my - sy) + my

    return (ax, ay)


# assume same kind of antenna
def locate_antinodes(pair: tuple[Coords, Coords]):
    a, b = pair
    return [locate_antinode(a, b), locate_antinode(b, a)]


def antinodes_for_bucket(bucket: set[Coords]):
    return itertools.chain.from_iterable(
        locate_antinodes(pair) for pair in itertools.combinations(bucket, 2)
    )


with open("input.txt", "r") as reader:
    grid = [list(line.strip()) for line in reader.readlines()]
    buckets: dict[str, set[Coords]] = dict()

    for y, line in enumerate(grid):
        for x, antenna in enumerate(line):
            if antenna != ".":
                bucket = buckets.get(antenna)
                if not bucket:
                    bucket = {(x, y)}
                    buckets[antenna] = bucket
                else:
                    bucket.add((x, y))

    antinodes = itertools.chain.from_iterable(
        antinodes_for_bucket(bucket) for bucket in buckets.values()
    )

    count = len(
        set(
            (x, y)
            for x, y in antinodes
            if x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)
        )
    )

    print(count)
