# https://adventofcode.com/2023/day/12

from typing import Iterable


def parse(lines: Iterable[str]):
    def parse_line(line: str):
        _bar, _counts = line.strip().split(None, 2)
        bar = [condition for condition in _bar]
        counts = [int(n) for n in _counts.split(",")]

        return bar, counts

    return [parse_line(line) for line in lines]


def trim(bar: list[str]):
    """
    >>> b = list('???.###'); ''.join(trim(b))
    '???.###'
    >>> b = list('.??..??...?##.'); ''.join(trim(b))
    '??..??...?##'
    >>> b = list('?#?#?#?#?#?#?#?'); ''.join(trim(b))
    '?#?#?#?#?#?#?#?'
    >>> b = list('????.#...#...'); ''.join(trim(b))
    '????.#...#'
    >>> b = list('????.######..#####.'); ''.join(trim(b))
    '????.######..#####'
    >>> b = list('?###????????'); ''.join(trim(b))
    '?###????????'
    """
    if len(bar) == 0:
        return bar

    if bar[0] == ".":
        return trim(bar[1:])
    elif bar[-1] == ".":
        return trim(bar[:-1])

    return bar


def should_reverse(bar: list[str], ledger: list[int]):
    """
    >>> b = list('???.###'); should_reverse(b, [1,1,3])
    True
    >>> b = list('??..??...?##'); should_reverse(b, [1,1,3])
    True
    >>> b = list('?#?#?#?#?#?#?#?'); should_reverse(b, [1,3,1,6])
    False
    >>> b = list('????.#...#'); should_reverse(b, [4,1,1])
    True
    >>> b = list('????.######..#####'); should_reverse(b, [1,6,5])
    True
    >>> b = list('?###????????'); should_reverse(b, [3,2,1])
    False
    """
    len_ledger = len(ledger)
    len_bar = len(bar)

    q, m = divmod(len_bar, len_ledger)
    if m > 0:
        q += 1

    head = bar[:q]
    tail = bar[-q:]

    count_head, count_tail = [len([x for x in b if x == "#"]) for b in (head, tail)]
    ledger_head, ledger_tail = ledger[0], ledger[-1]

    distance_head, distance_tail = (
        abs(count_head - ledger_head),
        abs(count_tail - ledger_tail),
    )

    if distance_head + count_tail > distance_tail + count_head:
        return True

    return False


workout_count = 0
workout_cache = {}


def workout(bar: list[str], broken_count: int) -> list[list[str]]:
    global workout_count
    workout_count += 1
    """
    eat up (the left side of) for the cases that matches with broken_count
    and spit out the smaller chunks for continuing
    empty list means all are eaten up

    reduce the number of permutations with heuristics

    >>> b = list('###'); workout(b, 3) # and [1, 1] still left
    [[]]

    # workout() will spit out only the still valid permutations
    # (excluding the unnecessary parts for further calculations)
    # e.g. `###` works already so it returns the rest
    >>> b = list('###.???'); workout(b, 3) # and [1, 1] still left
    [['?', '?', '?']]

    # e.g. 1. `#` works so it returns the rest
    #      2. `.#` works so it returns the rest
    #      3. `..#` works so it returns the rest
    >>> b = list('???'); workout(b, 1) # and [1] still left
    [['?'], [], []]

    # e.g. 1. `#` works so it returns the rest
    #      2. `.#` works so it returns the rest
    >>> b = list('??'); workout(b, 1) # and [] still left
    [[], []]

    # e.g. 1. `#` works so it returns the rest
    #      2. `.` doesn't work so it doesn't return
    >>> b = list('?'); workout(b, 1) # and [] still left
    [[]]

    # e.g. 1. `###` works so it returns the rest
    #      2. `##.` doesn't work so it doesn't return
    >>> b = list('##?...??..??'); workout(b, 3) # and [1, 1] still left
    [['?', '?', '.', '.', '?', '?']]

    # e.g. 1. `###` works so it returns the rest
    #      2. `##.` doesn't work so it doesn't return
    >>> b = list('??..??'); workout(b, 1) # and [1] still left
    [['?', '?'], ['?', '?'], [], []]

    # e.g. 1. `.#` works so it returns the rest
    #      2. `##` doesn't work so it doesn't return
    >>> b = list('?#?#?#?#?#?#?#?'); workout(b, 1) # and [3, 1, 6] still left
    [['#', '?', '#', '?', '#', '?', '#', '?', '#', '?', '#', '?']]

    >>> b = list('????.#...#...'); workout(b, 4) # and [1, 1]) still left
    [['#', '.', '.', '.', '#']]

    >>> b = list('???????'); workout(b, 2) # and [1] still left
    [['?', '?', '?', '?'], ['?', '?', '?'], ['?', '?'], ['?'], [], []]

    >>> b = list('.#?????#?#????'); workout(b, 1) # and [3] still left
    [['?', '?', '?', '?', '#', '?', '#', '?', '?', '?', '?']]

    >>> b = list('????#?#????'); workout(b, 3) # and [] still left
    [['#', '?', '#', '?', '?', '?', '?'], ['#', '?', '?', '?', '?'], ['?', '?', '?']]

    # the result above looks weird but it's actually right as `workout` doesn't have the information on what's left to check
    """

    cache_key = f"{bar},{broken_count}"
    cached = workout_cache.get(cache_key, None)

    if cached:
        return cached

    def with_cache(result):
        workout_cache[cache_key] = result
        print("work_out_cache", len(workout_cache))
        return result

    # early exit when there is no point to continue
    if len(bar) == 0:
        return with_cache([])

    def count_first_broken_chunk(bar: list[str]):
        count = 0
        for spring in bar:
            if spring == "#":
                count += 1
            else:
                return count

        return count

    # handle when actual_count (count_first_chunk(bar)) is already matching with broken_count
    if bar[0] == "#":
        actual_count = count_first_broken_chunk(bar)

        if actual_count > broken_count:
            return with_cache([])
        elif actual_count == broken_count:
            # '?' next completed broken set cannot be '#' hence it must be '.'
            # and '.' on the edge is trimmable
            if len(bar) > broken_count and bar[broken_count] == "?":
                return with_cache([trim(bar[broken_count + 1 :])])
            # if all is complete this will be empty list: [[]]
            return with_cache([trim(bar[broken_count:])])

    try:
        idx_to_permutate = bar.index("?")
    except:
        # when no permutations possible

        # detect a case like this `##.` and 3 as broken count
        if bar[0] == "#" and count_first_broken_chunk(bar) < broken_count:
            return with_cache([])

        return with_cache([bar])

    # detect a case like this `##.?` and 3 as broken count
    if bar[0] == "#" and "." in bar and bar.index("?") > bar.index("."):
        # if bar[0] == '#' and count_first_chunk(bar) < idx_to_permutate-1:
        return with_cache(
            []
        )  # this is indicating that no possibilities are found and it is different from [[]]

    head, tail = bar[:idx_to_permutate], bar[idx_to_permutate + 1 :]

    perms = [
        head + ["#"] + tail,
        head + ["."] + tail,
    ]

    # keep traversing until concluded
    return with_cache([p for perm in perms for p in workout(trim(perm), broken_count)])


def reverse_to_favor_starting_with_pound(b: list[str]):
    if b[-1] == "#" and b[0] != "#":
        return list(reversed(b))

    return b


# do this for everytime
# maybe workout should accept one more future count and -1 (to indicate no more)
# to eliminate more cases earlier
# before this
# was the answer for 525152 sample1 and 3836234 is how many times workout was called
# let's see how much this gets reduced after


def workout_for_final(bar: list[str], broken_count: int):
    """
    >>> b = list('????#?#????'); workout_for_final(b, 3)
    [['?', '?', '?']]
    """

    return [
        final
        for final in workout(reverse_to_favor_starting_with_pound(bar), broken_count)
        if not any([True if spring == "#" else False for spring in final])
    ]


d_and_c_cache = {}


# this seem to be better than the brute force version `count_matches`
# at least in memory efficiency
# but unfortunately it still struggles with bigger size
def divide_and_conquer(bar: list[str], ledger: list[int]):
    """
    >>> b = list('???.###'); divide_and_conquer(b, [1, 1, 3])
    1
    >>> b = list('.??..??...?##.'); divide_and_conquer(b, [1, 1, 3])
    4
    >>> b = list('?#?#?#?#?#?#?#?'); divide_and_conquer(b, [1, 3, 1, 6])
    1
    >>> b = list('????.#...#...'); divide_and_conquer(b, [4, 1, 1])
    1
    >>> b = list('????.######..#####.'); divide_and_conquer(b, [1, 6, 5])
    4
    >>> b = list('?###????????'); divide_and_conquer(b, [3, 2, 1])
    10
    """
    cache_key = f"{bar},{ledger}"
    cached = d_and_c_cache.get(cache_key, None)

    if cached:
        return cached

    def with_cache(result):
        d_and_c_cache[cache_key] = result

        print("d_and_c_cache", len(d_and_c_cache))
        return result

    bar = trim(bar)

    if should_reverse(bar, ledger):
        bar, ledger = list(reversed(bar)), list(reversed(ledger))

    first_chunk_length = ledger[0]

    candidates = workout(bar, first_chunk_length)

    rest = ledger[1:]

    # time to count as there is only last set to check
    # reuse `count_matches` from part 1 as this point shouldn't require highly optimized code
    if len(rest) == 1:
        # filter out empty ones because that means it already doesn't qualify
        return with_cache(
            sum(
                len(workout_for_final(cand, rest[0]))
                for cand in candidates
                if len(cand) > 0
            )
        )
        # return sum(count_matches(cand, rest) for cand in candidates if len(cand) > 0)

    # repeat reducing until it there is only last one left
    return with_cache(
        sum(divide_and_conquer(candidate, rest) for candidate in candidates)
    )


def handle_multiple_via_heuristics(bar: list[str], ledger: list[int], to_multiply: int):
    def multiply(rate: int):
        return ((bar + ["?"]) * rate)[:-1], ledger * rate

    return divide_and_conquer(*multiply(to_multiply))


with open("input.txt", "r") as reader:
    parsed = parse(reader.readlines())

    answer = sum(
        handle_multiple_via_heuristics(bar, ledger, 5) for bar, ledger in parsed
    )

    print(answer)
    print(workout_count)


def run_doctests():
    import doctest

    if doctest.testmod().failed:
        raise Exception("doc test failed")


if __name__ == "__main__":
    run_doctests()
