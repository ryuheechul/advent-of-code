# https://adventofcode.com/2024/day/14

# find part 1 at ./part1.py
# find part 2 at ./part2.py

Coords = tuple[int, int]
Velocity = tuple[int, int]
Tiles = tuple[int, int]


class Bot:
    coords: Coords
    velocity: Velocity
    tiles: Tiles

    def __init__(self, coords: Coords, velocity: Velocity, tiles: Tiles):
        self.coords = coords
        self.velocity = velocity
        self.tiles = tiles

    def move(self):
        x, y = self.coords
        vx, vy = self.velocity
        tx, ty = self.tiles

        nx, ny = x + vx, y + vy

        if nx >= tx:
            nx -= tx
        if ny >= ty:
            ny -= ty
        if nx < 0:
            nx += tx
        if ny < 0:
            ny += ty

        self.coords = nx, ny

    def __str__(self) -> str:
        return str(self.coords)


def parse(line: str, tiles: Tiles):
    def numbers(chunk: str):
        x, y = [int(s) for s in chunk.split("=", 1)[1].split(",", 1)]
        return x, y

    position, velocity = [numbers(chunk) for chunk in line.split(maxsplit=1)]
    return Bot(position, velocity, tiles)


filename, tiles = [("sample1.txt", (11, 7)), ("input.txt", (101, 103))][1]

with open(filename, "r") as reader:
    bots = [parse(line.strip(), tiles) for line in reader.readlines()]

    for _ in range(100):
        for bot in bots:
            bot.move()

    tx, ty = tiles
    mx, my = [int((t - 1) / 2) for t in tiles]

    sections = [
        # left top
        ((0, mx - 1), (0, my - 1)),
        # right top
        ((mx + 1, tx - 1), (0, my - 1)),
        # left bottom
        ((0, mx - 1), (my + 1, ty - 1)),
        # right bottom
        ((mx + 1, tx - 1), (my + 1, ty - 1)),
    ]

    bucket = {section: 0 for section in sections}

    for bot in bots:
        x, y = bot.coords

        for section in sections:
            x_range, y_range = section
            lx, rx = x_range
            ty, by = y_range

            if x >= lx and x <= rx and y >= ty and y <= by:
                bucket[section] += 1
                break

    import math

    p = math.prod(n for n in bucket.values())

    print(p)
