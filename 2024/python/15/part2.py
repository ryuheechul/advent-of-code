# https://adventofcode.com/2024/day/15

# find part 1 at ./part1.py
# find part 2 at ./part2.py

from enum import Enum


class Symbol(Enum):
    Left = "<"
    Right = ">"
    Up = "^"
    Down = "v"
    BoxLeft = "["
    BoxRight = "]"
    Wall = "#"
    Bot = "@"
    Space = "."


def construct(lines: list[str]):
    def convert(spot: str):
        match spot:
            case "#":
                return "##"
            case ".":
                return ".."
            case "@":
                return "@."
            case "O":
                return "[]"

        raise ValueError("wrong map?")

    expanded = [[c for spot in line for c in convert(spot)] for line in lines]

    for y, line in enumerate(expanded):
        for x, spot in enumerate(line):
            if spot == Symbol.Bot.value:
                return [list(line) for line in expanded], (x, y)

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


def move_down(force_coords: tuple[int, int], grid: list[list[str]]):
    x, y = force_coords
    len_column = len(grid)

    layers = [{x}]
    current_layer = {x}
    cy = y + 1
    while cy < len_column:
        new_layer = set()
        for cx in current_layer:
            object_below = grid[cy][cx]

            match Symbol(object_below):
                case Symbol.Wall:
                    continue
                case Symbol.Space:
                    continue
                case Symbol.BoxLeft:
                    new_layer.add(cx)
                    new_layer.add(cx + 1)
                case Symbol.BoxRight:
                    new_layer.add(cx)
                    new_layer.add(cx - 1)

        if not len(new_layer):
            break

        layers.append(new_layer)
        current_layer = new_layer
        cy += 1

    # collect all the things (with above) to move down with set so same coords that are pointed from two different boxes are not moved twice;
    # and execute moving by each layer from the bottom
    for cy, layer in reversed([(n + y, layer) for n, layer in enumerate(layers)]):
        by = cy + 1
        for cx in layer:
            # swap
            to_below, to_above = grid[cy][cx], grid[by][cx]
            grid[cy][cx], grid[by][cx] = to_above, to_below

    return grid


def can_move_down(force_coords: tuple[int, int], grid: list[list[str]]):
    x, y = force_coords

    # when no more to proceed - which is unnecessary due to the wall layer but why not
    if y == len(grid) - 1:
        return False

    object_below = grid[y + 1][x]

    match Symbol(object_below):
        case Symbol.Space:
            return True
        case Symbol.Wall:
            return False
        case Symbol.BoxLeft:
            return all(
                can_move_down((nx, ny), grid) for nx, ny in [(x, y + 1), (x + 1, y + 1)]
            )
        case Symbol.BoxRight:
            return all(
                can_move_down((nx, ny), grid) for nx, ny in [(x - 1, y + 1), (x, y + 1)]
            )

    raise ValueError("should not be possible")


def move_vertical(direction: str, bot_coords: tuple[int, int], grid: list[list[str]]):
    match Symbol(direction):
        case Symbol.Up:
            x, y = bot_coords
            ry = len(grid) - y - 1
            flipped_coods, flipped_grid = move_vertical(
                Symbol.Down.value, (x, ry), list(reversed(grid))
            )
            x, ry = flipped_coods
            y = len(grid) - ry - 1

            return (x, y), list(reversed(flipped_grid))

    if can_move_down(bot_coords, grid):
        move_down(bot_coords, grid)
        x, y = bot_coords
        return (x, y + 1), grid

    return bot_coords, grid


def move(direction: str, bot_coords: tuple[int, int], grid: list[list[str]]):
    x, y = bot_coords
    chamber = []
    match Symbol(direction):
        case Symbol.Left:
            chamber = list(reversed(grid[y][: (x + 1)]))
        case Symbol.Right:
            chamber = grid[y][x:]
        case Symbol.Up:
            return move_vertical(direction, bot_coords, grid)
        case Symbol.Down:
            return move_vertical(direction, bot_coords, grid)

    rearranged = move_right(chamber)

    match Symbol(direction):
        case Symbol.Left:
            grid[y][: (x + 1)] = reversed(rearranged)
        case Symbol.Right:
            grid[y][x:] = rearranged

    if rearranged != chamber:
        match Symbol(direction):
            case Symbol.Left:
                bot_coords = (x - 1, y)
            case Symbol.Right:
                bot_coords = (x + 1, y)

    return bot_coords, grid


def sum_gps(grid: list[list[str]]):
    return sum(
        y * 100 + x
        for y, line in enumerate(grid)
        for x, spot in enumerate(line)
        if Symbol(spot) == Symbol.BoxLeft
    )


filename = ["sample1.txt", "sample2.txt", "sample3.txt", "input.txt"][3]


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
