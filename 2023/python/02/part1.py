# https://adventofcode.com/2023/day/2

red, green, blue = 'red', 'green', 'blue'

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
    n, name = cube.split(' ')
    return Cube(name, int(n))

def parse_bag(bag: str):
    items = bag.split(', ')
    cubes = [parse_cube(item) for item in items]

    return cubes

def parse_body(body: str):
    stripped = body.strip()
    chunks = stripped.split('; ')
    bags = [parse_bag(chunk) for chunk in chunks]

    return bags

def parse_head(head: str):
    import re
    index = re.search(r'\d+', head)

    if index is None:
        raise Exception("Couldn't parse game")

    return int(index.group())

def parse_game(line: str):
    head, body = line.split(': ', 2)
    index, body = parse_head(head), parse_body(body)
    return index, body

def test_bag(bag: list[Cube]):
    for cube in bag:
        if constraint[cube.name] < cube.count:
            return False

    return True

def test_possible(bags):
    for bag in bags:
        if not test_bag(bag):
            return False

    return True

def score(index, bags):
    if test_possible(bags):
        return index
    return 0

with open('input.txt', 'r') as reader:
    total_score = 0
    for line in reader.readlines():
        total_score += score(*parse_game(line))

    print(total_score)
