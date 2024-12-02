# https://adventofcode.com/2024/day/2


from typing import Iterable


def scores(line: str):
    return [int(c) for c in line.split()]


def _is_safe(scores: Iterable[int]):
    prev: int | None = None
    diff: int | None = None
    prev_diff: int | None = None

    for score in scores:
        if prev:
            if diff:
                prev_diff = diff

            diff = score - prev

            # if it's not gradual
            if abs(diff) > 3 or diff == 0:
                return False

            if prev_diff:
                # if direction has changed
                if (abs(diff) == diff) != (abs(prev_diff) == prev_diff):
                    return False

            prev = score
        else:
            prev = score
            continue

    return True


def is_safe(scores: list[int]):
    import itertools

    return sum(_is_safe(t) for t in itertools.combinations(scores, len(scores) - 1)) > 0


with open("input.txt", "r") as reader:
    s = sum(
        is_safe(scores(line)) for line in reader.readlines() if len(line.strip()) > 0
    )
    print(s)
