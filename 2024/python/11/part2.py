# https://adventofcode.com/2024/day/11


# ./part1.py method, it will take too long (for example) for level 75

# these is the crucial dictionary cache for big levels to both save memory and computations
junction_level_count_cache: dict[tuple[int, int], int] = dict()


def apply_rule(stone: int):
    if stone == 0:
        return [1]

    stone_text = str(stone)
    len_stone_text = len(stone_text)
    if len_stone_text % 2 == 0:
        half_len = int(len_stone_text / 2)

        return [int(n) for n in (stone_text[0:half_len], stone_text[half_len:])]

    return [stone * 2024]


def construct_junctions(level: int, stone: int):
    bucket = set(apply_rule(stone))

    for level in reversed(range(level)):
        to_iter = list(bucket)
        bucket = set()

        for s in to_iter:
            for st in apply_rule(s):
                bucket.add(st)


# recursion will only happen in X level deep
def count(level: int, stone: int):
    if level == 0:
        return 1

    key = (stone, level)
    cached = junction_level_count_cache.get(key)

    if cached:
        return cached

    counted = sum(count(level - 1, s) for s in apply_rule(stone))

    junction_level_count_cache[key] = counted

    return counted


filename = ["sample1.txt", "input.txt"][1]
with open(filename, "r") as reader:
    line = next(iter(reader.readlines()))
    stones = [int(n) for n in line.strip().split()]
    level = 75

    for stone in stones:
        construct_junctions(level, stone)

    s = sum(count(level, stone) for stone in stones)

    print(s)
