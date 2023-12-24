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


def count_until_zzz(
    infinite_instructions_gen: Callable[[], Iterable[str]],
    nodes: dict[str, dict[str, str]],
):
    infinite_instructions = infinite_instructions_gen()
    next = nodes["AAA"]
    for idx, ins in enumerate(infinite_instructions):
        key_for_next = next[ins]

        if key_for_next == "ZZZ":
            return idx + 1

        next = nodes[key_for_next]


if __name__ == "__main__":
    ins, nodes = parse()

    answer = count_until_zzz(ins, nodes)

    print(answer)
