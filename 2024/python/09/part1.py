# https://adventofcode.com/2024/day/9

from typing import Iterable
import itertools


def fill_left(blocks: list[str], total_files: int):
    reversed_blocks = reversed(blocks)

    iter_this = (
        (idx, block) for idx, block in enumerate(reversed_blocks) if block != "."
    )

    def fill(block: str):
        if block == ".":
            _, b = next(iter_this)
            return b

        return block

    # no need to advance after it's covered for the length of total_files
    return itertools.islice((fill(b) for b in blocks), total_files)


def to_block(digits: Iterable[int]):
    head, *rest = digits

    free_spaces = rest[::2]
    files = rest[1::2]

    sum_of_files = head + sum(files)

    # this can't be joined as a string because the ID will soon become two+ digits after 9
    result = (head * [str(0)]) + list(
        itertools.chain.from_iterable(
            (["."] * free) + ([str(i + 1)] * file)
            for i, (free, file) in enumerate(zip(free_spaces, files))
        )
    )
    return (
        result,
        sum_of_files,
    )


def checksum(blocks: Iterable[str]):
    return sum(int(digit_str) * idx for idx, digit_str in enumerate(blocks))


filename = ["sample1.txt", "input.txt"][1]

with open(filename, "r") as reader:
    # actual input is just one line but I made it to work with multiple lines and sum if any
    blocks_set = (
        to_block(int(digit) for digit in line.strip()) for line in reader.readlines()
    )

    s = sum(checksum(fill_left(b, total_files)) for b, total_files in blocks_set)
    print(s)
