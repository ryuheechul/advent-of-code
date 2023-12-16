# https://adventofcode.com/2023/day/1

import re

word_map = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def translate(word):
    return word_map.get(word, word)


def filter_numbers(line):
    found = re.findall(
        # use look ahead `(?=...)` to include overlapped ones
        # https://www.reddit.com/r/adventofcode/comments/188wjj8/2023_day_1_did_not_see_this_coming/
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Lookahead_assertion
        r"(?=([0-9]|zero|one|two|three|four|five|six|seven|eight|nine))",
        line,
    )
    numerized = [int(translated) for translated in (translate(f) for f in found)]
    return numerized


def gen_two_digits(line):
    ns = filter_numbers(line)
    return ns[0] * 10 + ns[-1]


with open("input.txt", "r") as reader:
    sum = 0
    for line in reader:
        sum += gen_two_digits(line)

    print(sum)
