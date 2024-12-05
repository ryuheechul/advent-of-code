# https://adventofcode.com/2024/day/4

# type
Coords = tuple[int, int]
# type
Grid = list[list[str]]
# type
Steps = list[Coords]

xmas = list("XMAS")


def add(c1: Coords, c2: Coords):
    x1, y1 = c1
    x2, y2 = c2
    return (x1 + x2, y1 + y2)


def check(
    grid: Grid,
    coords: Coords,
    letter: str,
):
    x, y = coords
    return grid[y][x] == letter


def search(grid: Grid, start: Coords, steps: Steps):
    to_search = zip(xmas, steps)

    return (
        sum(check(grid, add(start, coords), letter) for letter, coords in to_search)
        == 4
    )


def search_all(grid: Grid, coords: Coords):
    x, y = coords
    len_y = len(grid)
    len_x = len(grid[0])

    all = []

    #  0 1 2 3
    #        x
    #   x-2
    #
    #  0 1 2 3 4
    #          x
    #     x-2
    #
    #  0 1 2 3
    #      x
    # x-2
    safe_left = x - 2 > 0
    safe_top = y - 2 > 0

    #  0 1 2 3 4 5 [6]
    #      x
    #              len_x
    #
    #  0 1 2 3 4 5 [6]
    #        x
    #              len_x
    safe_right = x + 3 < len_x
    safe_bottom = y + 3 < len_y

    if safe_left:
        all.append([(0, 0), (-1, 0), (-2, 0), (-3, 0)])

    if safe_right:
        all.append([(0, 0), (1, 0), (2, 0), (3, 0)])

    if safe_top:
        all.append([(0, 0), (0, -1), (0, -2), (0, -3)])

    if safe_bottom:
        all.append([(0, 0), (0, 1), (0, 2), (0, 3)])

    if safe_left and safe_top:
        all.append([(0, 0), (-1, -1), (-2, -2), (-3, -3)])

    if safe_left and safe_bottom:
        all.append([(0, 0), (-1, 1), (-2, 2), (-3, 3)])

    if safe_right and safe_top:
        all.append([(0, 0), (1, -1), (2, -2), (3, -3)])

    if safe_right and safe_bottom:
        all.append([(0, 0), (1, 1), (2, 2), (3, 3)])

    return sum(search(grid, coords, s) for s in all)


def count_xmas(grid: Grid, coords: Coords) -> int:
    if not check(grid, coords, "X"):
        return 0

    return search_all(grid, coords)


with open("input.txt", "r") as reader:
    grid = [list(line.strip()) for line in reader.readlines()]

    s = sum(
        sum(count_xmas(grid, (x, y)) for x, _ in enumerate(line))
        for y, line in enumerate(grid)
    )
    print(s)
