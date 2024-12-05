# https://adventofcode.com/2024/day/4

# type
Coords = tuple[int, int]
# type
Grid = list[list[str]]
# type
Steps = list[Coords]

mas = list("MAS")
rmas = list(reversed(mas))


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


def _search(grid: Grid, start: Coords, steps: Steps, word: list[str]):
    to_search = zip(word, steps)

    return sum(
        check(grid, add(start, coords), letter) for letter, coords in to_search
    ) == len(mas)


def search(grid: Grid, start: Coords, steps: Steps):
    return _search(grid, start, steps, mas) or _search(grid, start, steps, rmas)


def search_all(grid: Grid, coords: Coords):
    x, y = coords
    len_y = len(grid)
    len_x = len(grid[0])

    all = []

    #  0 1 2 3
    #    x
    #  x-1
    #
    safe_left = x > 0
    safe_top = y > 0

    #  0 1 2 [3]
    #    x
    #        len_x
    safe_right = x + 1 < len_x
    safe_bottom = y + 1 < len_y

    safe = safe_left and safe_right and safe_top and safe_bottom

    if not safe:
        return 0

    #      0    1   2
    # 0  -1,-1     1,-1
    # 1        x,y
    # 2  -1,1      1,1
    all.append([(1, 1), (0, 0), (-1, -1)])
    all.append([(-1, 1), (0, 0), (1, -1)])

    return 1 if sum(search(grid, coords, s) for s in all) == 2 else 0


def count_xmas(grid: Grid, coords: Coords) -> int:
    if not check(grid, coords, "A"):
        return 0

    return search_all(grid, coords)


with open("input.txt", "r") as reader:
    grid = [list(line.strip()) for line in reader.readlines()]

    s = sum(
        sum(count_xmas(grid, (x, y)) for x, _ in enumerate(line))
        for y, line in enumerate(grid)
    )
    print(s)
