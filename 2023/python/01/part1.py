# https://adventofcode.com/2023/day/1

import re

def filter_numbers(line):
    return (int(s) for s in re.findall('[0-9]', line))

def gen_two_digits(line):
    ns = list(filter_numbers(line))
    return ns[0] * 10 + ns[-1]

with open('input.txt', 'r') as reader:
    sum = 0
    for line in reader:
        sum += gen_two_digits(line)

    print(sum)
