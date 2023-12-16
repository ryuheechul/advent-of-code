# https://adventofcode.com/2023/day/2

red, green, blue = "red", "green", "blue"

from dataclasses import dataclass


@dataclass
class Cube:
    name: str
    count: int


constraint = {
    red: 12,
    green: 13,
    blue: 14,
}


def parse_cube(cube: str):
    n, name = cube.split(" ")
    return Cube(name, int(n))


def parse_bag(bag: str):
    items = bag.split(", ")
    cubes = [parse_cube(item) for item in items]

    return cubes


def parse_body(body: str):
    stripped = body.strip()
    chunks = stripped.split("; ")
    bags = [parse_bag(chunk) for chunk in chunks]

    return bags


def parse_head(head: str):
    import re

    index = re.search(r"\d+", head)

    if index is None:
        raise Exception("Couldn't parse game")

    return int(index.group())


def parse_game(line: str):
    head, body = line.split(": ", 2)
    index, body = parse_head(head), parse_body(body)
    return index, body


def calc_power(bags: list[list[Cube]]):
    acc = {
        red: [],
        green: [],
        blue: [],
    }

    for bag in bags:
        for cube in bag:
            acc[cube.name].append(cube.count)

    maxes = []
    for counts in acc.values():
        # print(counts)
        maxes.append(max(counts))

    import math

    return math.prod(maxes)


def score(bags):
    return calc_power(bags)


with open("input.txt", "r") as reader:
    total_score = 0
    for line in reader.readlines():
        total_score += score(parse_game(line)[1])

    print(total_score)
