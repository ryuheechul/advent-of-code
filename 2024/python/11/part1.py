# https://adventofcode.com/2024/day/11


def apply_rule(stone: int):
    if stone == 0:
        return [1]

    stone_text = str(stone)
    len_stone_text = len(stone_text)
    if len_stone_text % 2 == 0:
        half_len = int(len_stone_text / 2)

        return [int(n) for n in (stone_text[0:half_len], stone_text[half_len:])]

    return [stone * 2024]


filename = ["sample1.txt", "input.txt"][1]
with open(filename, "r") as reader:
    line = next(iter(reader.readlines()))
    stones = [int(n) for n in line.strip().split()]

    for _ in range(25):
        stones = [s for stone in stones for s in apply_rule(stone)]

    print(len(stones))
