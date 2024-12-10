# https://adventofcode.com/2024/day/9

from typing import Iterable
import itertools


def extract_spaces(blocks: list[str]):
    started = -1
    last_i = 0

    for i, block in enumerate(blocks):
        last_i = i
        if block == ".":
            if started == -1:
                started = i
        else:
            if started == -1:
                continue

            yield (started, i - started)
            started = -1

    if started > 0:
        yield (started, last_i + 1 - started)


def extract_files(blocks: Iterable[str]):
    ignore_spaces = ((i, b) for i, b in enumerate(blocks) if b != ".")
    index, id = next(ignore_spaces)

    bucket = [id]

    last_index = index

    for index, block in ignore_spaces:
        if id == block:
            bucket.append(block)
        else:
            yield (last_index, bucket)
            id = block
            bucket = [id]

        last_index = index

    if bucket:
        yield (last_index, bucket)


# assuming files is constructed with a same digit char
def extract_id_from_files(files: list[str]):
    return int(files[0])


def pass_fitting_whole(
    reversed_blocks: Iterable[str],
    spaces: list[tuple[int, int]],
    id_to_resume: int,
):
    should_skip = True if id_to_resume > 0 else False

    for files_with_index in extract_files(reversed_blocks):
        _, files = files_with_index

        if extract_id_from_files(files) < id_to_resume:
            should_skip = False

        if should_skip:
            continue

        len_files = len(files)

        for idx_of_blocks, length in spaces:
            if length >= len_files:
                # this can be used to alter blocks outside
                yield idx_of_blocks, files_with_index

                break


def fill_left(blocks: list[str]):
    id_to_resume = -1
    while id_to_resume == -1 or id_to_resume > 0:
        spaces = list(extract_spaces(blocks))

        reversed_blocks = reversed(blocks)

        for idx, (reversed_idx, files) in pass_fitting_whole(
            reversed_blocks, spaces, id_to_resume
        ):
            # necessary to have this to mark where we are starting over and to know when to exit the while loop
            id_to_resume = extract_id_from_files(files)

            fixed_right_index = len(blocks) - reversed_idx - 1

            # files shouldn't move to the right
            if fixed_right_index < idx:
                break

            # move blocks
            blocks[idx : idx + len(files)] = files
            blocks[fixed_right_index : fixed_right_index + len(files)] = [
                "." for _ in range(len(files))
            ]

            # once we move blocks, this for loop is not accurate any more so need to start over with while loop
            break

    return blocks


def to_block(digits: Iterable[int]):
    head, *rest = digits

    free_spaces = rest[::2]
    files = rest[1::2]

    # this can't be joined as a string because the ID will soon become two+ digits after 9
    result = (head * [str(0)]) + list(
        itertools.chain.from_iterable(
            (["."] * free) + ([str(i + 1)] * file)
            for i, (free, file) in enumerate(zip(free_spaces, files))
        )
    )
    return result


def checksum(blocks: Iterable[str]):
    return sum(
        int(digit_str) * idx for idx, digit_str in enumerate(blocks) if digit_str != "."
    )


filename = ["sample1.txt", "input.txt"][1]

with open(filename, "r") as reader:
    # actual input is just one line but I made it to work with multiple lines and sum if any
    blocks_set = (
        to_block(int(digit) for digit in line.strip()) for line in reader.readlines()
    )

    s = sum(checksum(fill_left(b)) for b in blocks_set)
    print(s)
