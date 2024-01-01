# https://adventofcode.com/2023/day/10

from typing import Iterable


#  1
# 4P2
#  3
connected_directions_for: dict[str, set[int]] = {
    "-": {2, 4},
    "|": {1, 3},
    "L": {1, 2},
    "J": {1, 4},
    "7": {3, 4},
    "F": {2, 3},
    ".": set(),
    "S": {1, 2, 3, 4},
}

reversed_connected_directions_for = {
    f"{sorted(v)}": k for k, v in connected_directions_for.items()
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

    start_pipe_shape = set(
        n
        for n in [
            1 if 3 in up else 0,
            2 if 4 in right else 0,
            3 if 1 in down else 0,
            4 if 2 in left else 0,
        ]
        if n > 0
    )

    return pipe_map, start_pipe_coord, start_pipe_shape


def compress_v(p1, p2):
    match [p1, p2]:
        case ["7", "7"]:
            # note that ['-', '-'] is effectively equivalent to []
            return ["-", "-"]
        case ["7", "J"]:
            return ["-", "-"]
        case ["7", "L"]:
            return ["-"]
        case ["J", "J"]:
            return ["-", "-"]
        case ["J", "F"]:
            return ["-", "-"]
        case ["J", "7"]:
            return ["-", "-"]
        case ["L", "L"]:
            return ["-", "-"]
        case ["L", "F"]:
            return ["-", "-"]
        case ["L", "7"]:
            return ["-", "-"]
        case ["F", "F"]:
            return ["-", "-"]
        case ["F", "J"]:
            return ["-"]
        case ["F", "L"]:
            return ["-", "-"]
        case _:
            return []


def compress_h(p1, p2):
    match [p1, p2]:
        case ["7", "7"]:
            return ["|", "|"]
        case ["7", "L"]:
            return ["|"]
        case ["7", "F"]:
            return ["|", "|"]
        case ["J", "J"]:
            return ["|", "|"]
        case ["J", "L"]:
            return ["|", "|"]
        case ["J", "F"]:
            return ["|", "|"]
        case ["L", "L"]:
            return ["|", "|"]
        case ["L", "7"]:
            return ["|"]
        case ["L", "J"]:
            return ["|", "|"]
        case ["F", "F"]:
            return ["|", "|"]
        case ["F", "7"]:
            return ["|", "|"]
        case ["F", "J"]:
            return ["|"]
        case _:
            return []


# at a given point (x, y) you can ignore everything else but look only the lines that cross this point
# very similar to this way, https://www.reddit.com/r/adventofcode/comments/18f1sgh/comment/kcripvi/
# this function is not super efficient as it recalculate everything from scratch for each '.' but it does the job
def determine_inside(
    x: int, y: int, pipe_map: list[str], coords_map: dict[tuple[int, int], set[int]]
):
    vertical_len = len(pipe_map)
    horizontal_len = len(pipe_map[0])

    coords = coords_map.keys()

    vertical_pipe_properties = {1, 3}
    horizontal_pipe_properties = {2, 4}

    def check_if_target_has_any_property(target: tuple[int, int], properties: set[int]):
        if (pipe_property := coords_map.get(target)) is not None:
            return target in coords and len(pipe_property & properties) > 0

        return False

    # although it's counter-intuitive, we want pipes with horizontal properties for vertical lines
    pipes_to_check_vertically = [
        (x, y_prime, pipe_map[y_prime][x])
        for y_prime in range(vertical_len)
        if check_if_target_has_any_property((x, y_prime), horizontal_pipe_properties)
    ]

    pipes_to_check_horizontally = [
        (x_prime, y, pipe_map[y][x_prime])
        for x_prime in range(horizontal_len)
        if check_if_target_has_any_property((x_prime, y), vertical_pipe_properties)
    ]

    # early return when there is no prospect on further checking
    if len(pipes_to_check_vertically) == 0 or len(pipes_to_check_horizontally) == 0:
        return False

    # divide each line to two like below
    #
    #      uv
    #
    #  lh  x,y  rh
    #
    #      lv
    #
    upper_v = [p for _, my, p in pipes_to_check_vertically if my < y]
    lower_v = [p for _, my, p in pipes_to_check_vertically if my > y]
    left_h = [p for mx, _, p in pipes_to_check_horizontally if mx < x]
    right_h = [p for mx, _, p in pipes_to_check_horizontally if mx > x]

    def simplify(pipes, normal_pipe, compress):
        simplified = []
        candidate = None
        for p in pipes:
            if candidate:
                simplified.extend(compress(candidate, p))

                candidate = None
            elif p == normal_pipe:
                simplified.append(p)
            else:
                candidate = p

        if candidate:
            simplified.append(candidate)

        return simplified

    # corner pipes will be compressed into straight pipes
    upper_v, lower_v, left_h, right_h = [
        simplify(series, normal_pipe, compress)
        for series, normal_pipe, compress in [
            (upper_v, "-", compress_v),
            (lower_v, "-", compress_v),
            (left_h, "|", compress_h),
            (right_h, "|", compress_h),
        ]
    ]

    ok_from_up = len(upper_v) % 2 > 0
    ok_from_down = len(lower_v) % 2 > 0
    ok_from_left = len(left_h) % 2 > 0
    ok_from_right = len(right_h) % 2 > 0

    ok_from_vertical = ok_from_up and ok_from_down
    ok_from_horizontal = ok_from_left and ok_from_right

    # according to this, https://www.reddit.com/r/adventofcode/comments/18f1sgh/comment/kcripvi/
    # we don't need to check both vertical and horizontal but either is fine
    # but I leave this code alone as that's what I came up with
    if ok_from_vertical and ok_from_horizontal:
        return True

    return False


def count_insides(pipe_map: list[str], coords_for_loop: list[tuple[int, int]]):
    def clear_noise(y, l):
        return "".join(
            c if c == " " or (x, y) in coords_for_loop else "." for x, c in enumerate(l)
        )

    # NOTE: this is the part that I didn't think as something to do until later
    # which contributed for being stuck for a while
    # but by testing ./sample5.txt missing this part became apparent
    noise_free_pipe_map = [clear_noise(y, l) for y, l in enumerate(pipe_map)]

    coords_map = {
        # e.g. (2, 3): 'F'
        coord: connected_directions_for[pipe_map[coord[1]][coord[0]]]
        for coord in coords_for_loop
    }

    count = 0
    for y, line in enumerate(noise_free_pipe_map):
        for x, item in enumerate(line):
            if item == "." and determine_inside(x, y, noise_free_pipe_map, coords_map):
                count += 1

    return count


def traverse_the_loop(
    pipe_map: list[str], start_coord: tuple[int, int], start_pipe_shape: set[int]
):
    dx, dy = diff_for[next(iter(start_pipe_shape))]
    x, y = start_coord
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

            yield curr_coord

    # one for start and another for end
    coords_for_loop: list[tuple[int, int]] = [start_coord, next_to_start_coord]

    for coord in next_pipe(start_coord, next_to_start_coord):
        coords_for_loop.append(coord)

    return coords_for_loop


with open("input.txt", "r") as reader:
    pipe_map, start_pipe_coord, start_pipe_shape = parse(reader.readlines())

    coords_for_loop = traverse_the_loop(pipe_map, start_pipe_coord, start_pipe_shape)

    # replace S to a actual pipe character
    pipe_map[start_pipe_coord[1]] = "".join(
        c
        if start_pipe_coord[0] != idx
        else reversed_connected_directions_for[f"{sorted(start_pipe_shape)}"]
        for idx, c in enumerate(pipe_map[start_pipe_coord[1]])
    )

    answer = count_insides(pipe_map, coords_for_loop)

    print(answer)
