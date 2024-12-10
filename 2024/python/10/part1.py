# https://adventofcode.com/2024/day/10

Grid = list[list[int]]
Coords = tuple[int, int]


def find_trail_heads(grid: Grid):
    for y, line in enumerate(grid):
        for x, height in enumerate(line):
            if height == 0:
                yield (x, y)


def traverse(height: int, current: Coords, grid: Grid, visited_summits: set[Coords]):
    x, y = current
    ly = len(grid)
    lx = len(grid[0])

    if x < 0 or y < 0 or x > lx - 1 or y > ly - 1:
        return 0

    if grid[y][x] != height:
        return 0

    if height == 9:
        # ignore the ones already visited
        if current in visited_summits:
            return 0

        visited_summits.add(current)
        return 1

    north = x, y - 1
    east = x + 1, y
    south = x, y + 1
    west = x - 1, y

    return sum(
        traverse(height + 1, next_spot, grid, visited_summits)
        for next_spot in [north, east, south, west]
    )


def score(head: Coords, grid: Grid):
    return traverse(0, head, grid, set())


filename = ["sample1.txt", "input.txt"][1]
with open(filename, "r") as reader:
    grid = [[int(h) for h in line.strip()] for line in reader.readlines()]

    heads = list(find_trail_heads(grid))

    s = sum(score(head, grid) for head in heads)
    print(s)
