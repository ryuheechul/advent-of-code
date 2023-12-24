# https://adventofcode.com/2023/day/8

from typing import Callable, Iterable


def parse_instructions(line: str):
    instructions = line.strip()

    def infinite_iterator():
        while True:
            for instruction in instructions:
                yield instruction

    return infinite_iterator


def parse_node(line: str):
    node, right = line.strip().split(" = ", 2)
    l, r = right[1:-1].split(", ", 2)
    instructions = {"L": l, "R": r}

    return node, instructions


def parse():
    with open("input.txt", "r") as reader:
        ins = parse_instructions(reader.readline())
        _ = reader.readline()
        nodes = dict(parse_node(line) for line in reader.readlines())

        return ins, nodes


import re


def is_key_end_with_a(node: str):
    return bool(re.match(r"[A-Z0-9]{2}A$", node))


def is_key_end_with_z(node: str):
    return bool(re.match(r"[A-Z0-9]{2}Z$", node))


# after sensing that the brute force version (count_until_all_ending_with_z_brute_force) of this function would take forever
# I sought and found a hint here https://www.reddit.com/r/adventofcode/comments/18dh4p8/2023_day_8_part_2_im_a_bit_frustrated/
# on using https://en.wikipedia.org/wiki/Least_common_multiple
def count_until_all_ending_with_z(
    infinite_instructions_gen: Callable[[], Iterable[str]],
    nodes: dict[str, dict[str, str]],
):
    starts = [ins for key, ins in nodes.items() if is_key_end_with_a(key)]

    counts = []

    for start in starts:
        infinite_instructions = infinite_instructions_gen()
        next = start
        for idx, ins in enumerate(infinite_instructions):
            key_for_next = next[ins]

            if is_key_end_with_z(key_for_next):
                counts.append(idx + 1)
                break

            next = nodes[key_for_next]

    # https://stackoverflow.com/a/60822380/1570165
    import math

    return math.lcm(*counts)


# good luck with this one (with ./input.txt) but it works with ./sample3.txt though...
def count_until_all_ending_with_z_brute_force(
    infinite_instructions_gen: Callable[[], Iterable[str]],
    nodes: dict[str, dict[str, str]],
):
    infinite_instructions = infinite_instructions_gen()
    starts = [ins for key, ins in nodes.items() if is_key_end_with_a(key)]
    length = len(starts)

    currents = starts
    for idx, ins in enumerate(infinite_instructions):
        to_compare = 0
        nexts = []

        for curr in currents:
            key_for_next = curr[ins]

            if is_key_end_with_z(key_for_next):
                to_compare += 1

            nexts.append(nodes[key_for_next])

        if length == to_compare:
            return idx + 1

        currents = nexts


if __name__ == "__main__":
    ins, nodes = parse()

    answer = count_until_all_ending_with_z(ins, nodes)

    print(answer)
