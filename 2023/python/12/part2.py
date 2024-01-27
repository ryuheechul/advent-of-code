# based on https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day12p2.py
# and modified for my taste

# and my original attempt that I ended up giving up is at ./gave_up_attempt_on_part2.py

cache = {}


# gdcs: grouped_damaged_counts
# cds: conditions
def count(cds, gdcs):
    ## early exits
    # in case conditions are exhausted
    if cds == "":
        # if there is still grouped_damaged_counts left, then it's a impossible case, hence 0
        # if everything is exhausted at the same time we conclude that it's resolved, hence 1
        return 1 if gdcs == () else 0

    # in case there are still condition records are not exhausted but no more counts to compare with
    if gdcs == ():
        # if "#" still exist, it's impossible, hence 0
        # else it's considered to be resolved, hence 1
        return 0 if "#" in cds else 1
    ## end of early exits

    # avoid duplicated calculations with caching
    cache_key = (cds, gdcs)
    if cache_key in cache:
        return cache[cache_key]

    count_all = 0

    next_condition = cds[0]

    route_1 = 0
    # if the next_condition is assumed as `.`, simply ignore that
    if next_condition in ".?":
        trimmed = cds[1:]
        route_1 += count(trimmed, gdcs)

    route_2 = 0
    # if the next_condition is assumed as `#`, there can be only one case possible to continue
    # so find that out and move on
    if next_condition in "#?":
        next_count = gdcs[0]
        len_cds = len(cds)
        exact_length_scope = cds[:next_count]

        is_long_enough = next_count <= len_cds
        is_dot_not_ruining = "." not in exact_length_scope

        def not_pound_right_after():
            return cds[next_count] != "#"

        def is_grouping_possible():
            # `next_count == len_cds` is good because there is no next being `#` possible
            # `not_pound_right_after()` is good since at least one of possibility of `?` will result in no pound
            return next_count == len_cds or not_pound_right_after()

        if is_long_enough and is_dot_not_ruining and is_grouping_possible():
            next_to_count = cds[next_count + 1 :]
            tail_counts = gdcs[1:]

            route_2 += count(next_to_count, tail_counts)

    count_all = route_1 + route_2

    cache[cache_key] = count_all
    global count_cached
    return count_all


# gdcs: grouped_damaged_counts
# cds: conditions
to_multiply = 5


def parse_line(line: str):
    cds, gdcs = line.split()
    # use of tuple makes it hashable as list is unhashable
    gdcs = tuple(map(int, gdcs.split(",")))

    cds = "?".join([cds] * to_multiply)
    gdcs *= to_multiply

    return cds, gdcs


if __name__ == "__main__":
    with open("input.txt", "r") as reader:
        total = sum(count(*parse_line(line)) for line in reader.readlines())
        print(total)
