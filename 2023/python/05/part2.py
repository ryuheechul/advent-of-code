# https://adventofcode.com/2023/day/5

"""
# background
Not gonna lie, this one was puzzling... (you can see many people report that this part 2 was challenging)
And the my initial brute force (the code that was a slight change from ./part1.py) was expected to run for 6 hours.
After searching and watching some people's youtube videos, I got the hint on something to do with overlaps.

so instead of trying to map a single number with each row, a range will try and it can split up to 3
and 0-1 of them will be the one that is mapped and 0-2 them will be the ones are not mapped but splitted from the original range

figuring out overlaps is handled via `calc_row` from `./calc.py`
driving the splitting and splitted is handled via `calc_stage`.

In addition, instead of working with a different format between the row and target ("dest source length" and "target length"),
This is was pre computed like below to have lighter mental load on the parsing time
(diff, source_range(start, end)) and target_range(start, end)

# glossary
stage: a group of mapping rows. e.g. seed to soil
row: a single line that has mapping information. e.g. "dest source length"
target:
- it's a range that will compare to source range. e.g. `range(79, 93)`
- and it will be splitted to multiple targets for efficiency on each mapping
"""

from typing import Callable, Iterable


def parse(first_line: str, lines: Iterable[str]):
    """
    >>> parse(
    ...   "seeds: 79 14 55 13",
    ...   '''
    ... seed-to-soil map:
    ... 50 98 2
    ... 52 50 48
    ...
    ... soil-to-fertilizer map:
    ... 0 15 37
    ... 37 52 2
    ... 39 0 15
    ...   '''.split('\\n')
    ... )
    ([range(79, 93), range(55, 68)], [[(-48, range(98, 100)), (2, range(50, 98))], [(-15, range(15, 52)), (-15, range(52, 54)), (39, range(0, 15))]])
    """

    _, seeds = first_line.split(": ", 2)
    seeds_iter = (int(seed) for seed in seeds.split())

    # https://stackoverflow.com/a/4628446/1570165
    seed_targets = [
        range(start, start + length) for (start, length) in zip(seeds_iter, seeds_iter)
    ]

    stages = []
    stage = []
    for line in lines:
        if len(line) < 2:
            continue

        if not line[0].isdigit():
            if len(stage) > 0:
                stages.append(stage)

            stage = []
        else:
            dest, source, length = (int(s) for s in line.split(None, 3))

            # better values to help brain
            diff = dest - source
            length = range(source, source + length)
            stage.append((diff, length))

    # need to collect the last one at the end of the loop
    if len(stage) > 0:
        stages.append(stage)

    return seed_targets, stages


def calc_row_adapter(
    diff: int,
    source: range,
    target: range,
    submit_mapped: Callable[[list[range]], None],
):
    if __package__ is None or __package__ == "":
        from calc import calc_row
    else:
        from .calc import calc_row

    mapped, to_be_mapped = calc_row(diff, source, target)

    submit_mapped(mapped)
    return to_be_mapped


def calc_stage(stage: list[tuple[int, range]], target: range):
    """
    calc_stage is concerned only for each stage
    """
    targets: list[range] = [target]
    mapped: list[range] = []

    def add_to_mapped(to_be_added: list[range]):
        mapped.extend(to_be_added)

    # iterate over each row in a stage
    for diff, source in stage:
        # `mapped` will collect the ones completely mapped on each stage
        # `targets` will potentially keep splitting
        # and be flattened to be fed onto the next row
        targets = [
            next_target
            for target in targets
            for next_target in calc_row_adapter(diff, source, target, add_to_mapped)
        ]

        # early break when there is nothing left to try the rest of rows
        if len(targets) == 0:
            break

    # need to collect the last ones at the end of the loop
    if len(targets):
        mapped.extend(targets)

    return mapped


def calc_target(stages: list[list[tuple[int, range]]], target: range):
    """
    calc_target is concerned only for each target range
    """

    targets: list[range] = [target]

    for stage in stages:
        # https://realpython.com/python-flatten-list/#using-a-comprehension-to-flatten-a-list-of-lists
        targets = [item for t in targets for item in calc_stage(stage, t)]

    return min(in_item.start for in_item in targets)


def run():
    with open("input.txt", "r") as reader:
        seed_targets, stages = parse(reader.readline(), reader.readlines())

        answer = min(calc_target(stages, target) for target in seed_targets)

        return answer


def run_doctests():
    import doctest

    if doctest.testmod().failed:
        raise Exception("doc test failed")


if __name__ == "__main__":
    run_doctests()
    print(run())
