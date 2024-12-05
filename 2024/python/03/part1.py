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


def parse(line: str):
    regex = r"(mul\(\d+,\d+\))"
    regex2 = r"mul\((\d+),(\d+)\)"

    return [
        to_mul(matches[0])  # since there is just one
        for chunk in re.split(regex, line)
        if (matches := re.findall(regex2, chunk))
    ]


with open("input.txt", "r") as reader:
    answer = sum(
        sum(mul.multiply() for mul in parse(line)) for line in reader.readlines()
    )
    print(answer)
