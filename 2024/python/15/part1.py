# https://adventofcode.com/2024/day/15

# find part 1 at ./part1.py
# find part 2 at ./part2.py

from enum import Enum


class Symbol(Enum):
    Left = "<"
    Right = ">"
    Up = "^"
    Down = "v"
    Box = "O"
    Wall = "#"
    Bot = "@"
    Space = "."


def construct(lines: list[str]):
    for y, line in enumerate(lines):
        for x, spot in enumerate(line):
            if spot == Symbol.Bot.value:
                return [list(line) for line in lines], (x, y)

    raise ValueError("should never happen")


def move_right(chamber: list[str]):
    first_wall_index = chamber.index(Symbol.Wall.value)

    mutable, immutable = chamber[:first_wall_index], chamber[first_wall_index:]

    if len(mutable) < 2:
        return chamber

    if not any((it for it in mutable if Symbol(it) == Symbol.Space)):
        return chamber

    first_space_index = mutable.index(Symbol.Space.value)
    left, space, right = (
        mutable[:first_space_index],
        [Symbol.Space.value],
        mutable[first_space_index:][1:],
    )

    rearranged = space + left + right + immutable
    return rearranged


def move(direction: str, bot_coords: tuple[int, int], grid: list[list[str]]):
    x, y = bot_coords
    chamber = []
    match Symbol(direction):
        case Symbol.Left:
            chamber = list(reversed(grid[y][: (x + 1)]))
        case Symbol.Right:
            chamber = grid[y][x:]
        case Symbol.Up:
            chamber = list(
                reversed([line[x] for gy, line in enumerate(grid) if gy <= y])
            )
        case Symbol.Down:
            chamber = [line[x] for gy, line in enumerate(grid) if gy >= y]

    rearranged = move_right(chamber)

    match Symbol(direction):
        case Symbol.Left:
            grid[y][: (x + 1)] = reversed(rearranged)
        case Symbol.Right:
            grid[y][x:] = rearranged
        case Symbol.Up:
            flipped = list(reversed(rearranged))
            for gy, line in enumerate(grid):
                if gy <= y:
                    line[x] = flipped[gy]
        case Symbol.Down:
            chamber = [line[x] for gy, line in enumerate(grid) if gy >= y]
            for gy, line in enumerate(grid):
                if gy >= y:
                    line[x] = rearranged[gy - y]

    if rearranged != chamber:
        match Symbol(direction):
            case Symbol.Left:
                bot_coords = (x - 1, y)
            case Symbol.Right:
                bot_coords = (x + 1, y)
            case Symbol.Up:
                bot_coords = (x, y - 1)
            case Symbol.Down:
                bot_coords = (x, y + 1)

    return bot_coords, grid


def sum_gps(grid: list[list[str]]):
    return sum(
        y * 100 + x
        for y, line in enumerate(grid)
        for x, spot in enumerate(line)
        if Symbol(spot) == Symbol.Box
    )


filename = ["sample1.txt", "sample2.txt", "input.txt"][2]


with open(filename, "r") as reader:
    lines = [line.strip() for line in reader.readlines()]

    split_index = lines.index("")
    part1, part2 = lines[:split_index], lines[split_index + 1 :]

    grid, bot_coords = construct(part1)
    import itertools

    move_sequence = itertools.chain.from_iterable(part2)

    def debug_grid():
        for line in grid:
            print("".join(line))

    # debug_grid()
    for direction in move_sequence:
        bot_coords, grid = move(direction, bot_coords, grid)
        # debug_grid()

    s = sum_gps(grid)

    print(s)
