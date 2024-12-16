# https://adventofcode.com/2024/day/13

# find part 1 at ./part1.py
# find part 2 at ./part2.py

from typing import Iterable

Button = tuple[int, int]

filename = ["sample1.txt", "input.txt"][0]


def split(lines: Iterable[str]):
    count = 1
    acc = []

    try:
        while True:
            line = next(iter(lines))

            if count % 4 == 0:
                yield acc
                acc = []

            else:
                acc.append(line.strip())

            count += 1
    except Exception:
        if acc:
            yield acc
        return


def parse_button(line: str):
    def parse_button_n(text: str):
        return int(text.split("+", 1)[1])

    x, y = [
        parse_button_n(encoded_n) for encoded_n in line.split(": ", 1)[1].split(", ", 1)
    ]

    return (x, y)


def parse_prize(line: str):
    def parse_prize_n(text: str):
        return int(text.split("=", 1)[1])

    x, y = [
        parse_prize_n(encoded_n) for encoded_n in line.split(": ", 1)[1].split(", ", 1)
    ]

    return (x, y)


def parse(a: str, b: str, p: str):
    ba, bb = [parse_button(line) for line in [a, b]]

    prize = parse_prize(p)

    return ba, bb, prize


# example with:
# - ingredients: 1,3
# - n: 3
# - results: [[1, 1, 1], [1, 1, 3], [1, 3, 3], [3, 3, 3]]


def old_tries(n: int):
    # each button's cap is n not for the whole

    print(
        [
            [1 for _ in range(min(n - i, n))] + [3 for _ in range(min(i, n))]
            for i in range(n * n + 1)
        ]
    )
    return [
        [1 for _ in range(min(n - i, n))] + [3 for _ in range(min(i, n))]
        for i in range(n * n + 1)
    ]


def tries(n: int):
    max = n + 1
    return [[(1, i), (3, j)] for i in range(max) for j in range(max) if i > 0 or j > 0]


def all_tries_in_cheapest_order(n: int):
    import functools

    def score(n: list[tuple[int, int]]):
        return [cost * count for cost, count in n]

    def sort(a: list[tuple[int, int]], b: list[tuple[int, int]]):
        sa = score(a)
        sb = score(b)
        if sa < sb:
            return -1
        else:
            return 1

    return sorted(
        [combination for n in range(1, 1 + n) for combination in tries(n)],
        key=functools.cmp_to_key(sort),
    )


def does_bingo(
    a: Button, b: Button, prize: Button, compact_combination: list[tuple[int, int]]
):
    def extract_count(c: list[tuple[int, int]]):
        am, bm = 0, 0
        for n, count in c:
            if n == 1:
                bm = count
            elif n == 3:
                am = count

        return am, bm

    ax, ay = a
    bx, by = b
    am, bm = extract_count(compact_combination)
    px, py = prize

    a_multiplied_x, a_multiplied_y = ax * am, ay * am
    b_multiplied_x, b_multiplied_y = bx * bm, by * bm

    x_to_divide_with, y_to_divide_with = (
        a_multiplied_x + b_multiplied_x,
        a_multiplied_y + b_multiplied_y,
    )

    if (
        px % x_to_divide_with == 0
        and py % y_to_divide_with == 0
        and px / x_to_divide_with == py / y_to_divide_with
    ):
        # the factor has to be int with the condition above
        return True, int(px / x_to_divide_with)

    return False, 0


all_tries = all_tries_in_cheapest_order(100)


def find_cost(a: Button, b: Button, prize: Button):
    def _find_cost(c: list[tuple[int, int]]):
        return sum(n * count for n, count in c)

    for c in all_tries:
        bingo, factor = does_bingo(a, b, prize, c)
        if bingo:
            cost = _find_cost(c)
            # print(prize, a, b, c, cost * factor, cost, factor)
            return cost * factor

    return 0


with open(filename, "r") as reader:
    parsable = list(split(iter(reader.readlines())))

    # comment out to use `multiprocessing.Pool` instead to speed up
    # s = sum(find_cost(a, b, p) for a, b, p in [parse(*p) for p in parsable])
    # print(s)

    from multiprocessing import Pool

    with Pool() as p:
        s = sum(p.starmap(find_cost, [parse(*p) for p in parsable], chunksize=2))
        print(s)
