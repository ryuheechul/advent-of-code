# https://adventofcode.com/2024/day/11


# ./part1.py method, it will take too long (for example) for level 75

# these two dictionary caches are crucial for big levels to both save memory and computations
unique_junctions: dict[int, list[int]] = (
    dict()
)  # you will see that unique_junctions are actually not that much
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


def with_cache(stone: int):
    cached = unique_junctions.get(stone)

    if cached:
        return cached

    unique_junctions[stone] = apply_rule(stone)

    return unique_junctions[stone]


def construct_junctions(level: int, stone: int):
    bucket = set(with_cache(stone))

    for level in reversed(range(level)):
        to_iter = list(bucket)
        bucket = set()

        for s in to_iter:
            for st in with_cache(s):
                bucket.add(st)


# recursion will only happen in X level deep
def count(level: int, stone: int):
    if level == 0:
        return 1

    key = (stone, level)
    cached = junction_level_count_cache.get(key)

    if cached:
        return cached

    counted = sum(count(level - 1, s) for s in with_cache(stone))

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
