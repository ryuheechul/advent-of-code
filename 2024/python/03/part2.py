# https://adventofcode.com/2024/day/3

from dataclasses import dataclass
import re


@dataclass
class Mul:
    n: int
    m: int

    def multiply(self) -> int:
        return self.n * self.m


def to_mul(t: tuple[str, str]):
    _n, _m = t
    return Mul(int(_n), int(_m))


def _parse(line: str):
    regex = r"(mul\(\d+,\d+\))"
    regex2 = r"mul\((\d+),(\d+)\)"

    return [
        to_mul(matches[0])  # since there is just one
        for chunk in re.split(regex, line)
        if (matches := re.findall(regex2, chunk))
    ]


do = "do()"
dont = "don't()"


class DoDont:
    v = do

    @classmethod
    def next(cls):
        # alternate between `do` and `dont`
        cls.v = dont if cls.v == do else do

        return cls.v


def passthrough(s: str):
    return s


def block(_: str):
    return ""


def filter_do(line: str) -> str:
    filters = [block, filter_choose]
    delimiter = do

    return "".join(
        filtered
        for chunk, filter in zip(line.split(delimiter, 1), filters)
        if (filtered := filter(chunk))
    )


def filter_dont(line: str) -> str:
    filters = [passthrough, filter_choose]
    delimiter = dont

    return "".join(
        filtered
        for chunk, filter in zip(line.split(delimiter, 1), filters)
        if (filtered := filter(chunk))
    )


def filter_choose(line: str) -> str:
    next = DoDont.next()
    is_do = next == do

    # skip filtering if nothing to filter to begin with
    if next not in line:
        # reverse/restore the tick
        DoDont.next()

        # meaning it's still under influence of dont
        if is_do:
            return ""

        # meaning it's still under influence of do
        return line

    # start filtering with the right target
    if is_do:
        return filter_do(line)
    else:
        return filter_dont(line)


def parse(line: str):
    return _parse(filter_choose(line))


with open("input.txt", "r") as reader:
    answer = sum(
        sum(mul.multiply() for mul in parse(line)) for line in reader.readlines()
    )
    print(answer)
