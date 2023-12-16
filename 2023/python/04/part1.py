# https://adventofcode.com/2023/day/4


from typing import Iterable


def to_numbers(line: str):
    # split without args will or None as first arg will split on white space
    # https://stackoverflow.com/a/8113787/1570165
    return (int(s) for s in line.split())


def parse_line(line: str):
    _, numbers = line.split(": ", 2)

    winning, mine = (to_numbers(l) for l in numbers.split(" | ", 2))

    return winning, mine


def calc_score(winning: Iterable[int], mine: Iterable[int]):
    l = len(set(winning) & set(mine))
    if l < 1:
        return l

    b = l - 1
    return 2**b


with open("input.txt", "r") as reader:
    s = sum(calc_score(*parse_line(line)) for line in reader.readlines())
    print(s)
