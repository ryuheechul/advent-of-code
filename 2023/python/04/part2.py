# https://adventofcode.com/2023/day/4


from typing import Iterable


def to_numbers(line: str):
    # split without args will or None as first arg will split on white space
    # https://stackoverflow.com/a/8113787/1570165
    return (int(s) for s in line.split())


def parse_line(line: str):
    header, numbers = line.split(": ", 2)
    card_n = int(header.split(None, 2)[-1])

    winning, mine = (to_numbers(l) for l in numbers.split(" | ", 2))

    return card_n, winning, mine


def calc_nexts(card_n: int, winning: Iterable[int], mine: Iterable[int]):
    l = len(set(winning) & set(mine))
    how_many_nexts = l
    next = card_n + 1
    nexts = range(next, next + how_many_nexts)
    return card_n, nexts


with open("input.txt", "r") as reader:
    parsed = dict(calc_nexts(*parse_line(line)) for line in reader.readlines())

    acc = 0
    queue = list(parsed.keys())
    for n in queue:
        acc += 1
        l = parsed[n]
        if l:
            queue.extend(l)

    print(acc)
