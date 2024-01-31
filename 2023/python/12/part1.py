# https://adventofcode.com/2023/day/12

from typing import Iterable


def parse(lines: Iterable[str]):
    def parse_line(line: str):
        _bar, _counts = line.strip().split(None, 2)
        bar = [condition for condition in _bar]
        counts = [int(n) for n in _counts.split(",")]

        return bar, counts

    return [parse_line(line) for line in lines]


def permutate_conditions(bar: list[str]):
    try:
        idx = bar.index("?")
        left = bar[:idx]
        right = bar[idx + 1 :]
        first = left + ["."] + right
        second = left + ["#"] + right

        return [
            perm
            for perm_list in [permutate_conditions(first), permutate_conditions(second)]
            for perm in perm_list
        ]
    except Exception:
        return [bar]


# this is brute force and not efficient both for space and computation
def count_matches(bar: list[str], broken_consecutives: list[int]):
    perms = permutate_conditions(bar)

    def reconstruct(bar: list[str]):
        broken = 0
        bag = []
        for condition in bar:
            if condition == "#":
                broken += 1
            elif broken > 0:
                bag.append(broken)
                broken = 0
            else:
                pass

        if broken > 0:
            bag.append(broken)
        return bag

    return len([p for p in perms if reconstruct(p) == broken_consecutives])
    # consecutive


with open("input.txt", "r") as reader:
    parsed = parse(reader.readlines())

    answer = sum(count_matches(bar, ledger) for bar, ledger in parsed)

    print(answer)
