# https://adventofcode.com/2023/day/10

from typing import Iterable

#  1
# 4P2
#  3
connected_directions_for = {
    "-": {2, 4},
    "|": {1, 3},
    "L": {1, 2},
    "J": {1, 4},
    "7": {3, 4},
    "F": {2, 3},
    ".": set(),
    "S": {1, 2, 3, 4},
}

diff_for: dict[int, tuple[int, int]] = {
    #: (x, y)
    1: (0, -1),  # up
    2: (1, 0),  # right
    3: (0, 1),  # down
    4: (-1, 0),  # left
}

reversed_diff_for = {v: k for k, v in diff_for.items()}


def parse(lines: Iterable[str]):
    x, y = -1, -1
    pipe_map: list[str] = []
    for idx, line in enumerate(lines):
        pipe_map.append(line.strip())

        if "S" in line:
            x = line.index("S")
            y = idx

    start_pipe_coord = (x, y)

    # start = connected_directions_for[pipe_map[y][x]]
    left = connected_directions_for[pipe_map[y][x - 1]]
    right = connected_directions_for[pipe_map[y][x + 1]]
    up = connected_directions_for[pipe_map[y - 1][x]]
    down = connected_directions_for[pipe_map[y + 1][x]]

    s = set(
        n
        for n in [
            1 if 3 in up else 0,
            2 if 4 in right else 0,
            3 if 1 in down else 0,
            4 if 2 in left else 0,
        ]
        if n > 0
    )

    return pipe_map, start_pipe_coord, s


with open("input.txt", "r") as reader:
    pipe_map, start_pipe_coord, start_pipe_shape = parse(reader.readlines())

    dx, dy = diff_for[next(iter(start_pipe_shape))]
    x, y = start_pipe_coord
    next_to_start_coord = (x + dx, y + dy)

    def get_pipe(coord: tuple[int, int]):
        return connected_directions_for[pipe_map[coord[1]][coord[0]]]

    def next_pipe(prev_coord, curr_coord):
        while True:
            curr_pipe = get_pipe(curr_coord)

            cx, cy = curr_coord
            px, py = prev_coord

            to_exclude = {reversed_diff_for[(px - cx, py - cy)]}

            move_to = curr_pipe - to_exclude
            dx, dy = diff_for[next(iter(move_to))]

            prev_coord = curr_coord
            curr_coord = (cx + dx, cy + dy)

            curr_pipe = get_pipe(curr_coord)

            if len(curr_pipe) == 4:
                return

            yield curr_pipe

    # one for start and another for end
    distance = 2

    for pipe in next_pipe(start_pipe_coord, next_to_start_coord):
        distance += 1

    answer = int(distance / 2)

    print(answer)
