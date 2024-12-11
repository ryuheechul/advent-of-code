# https://adventofcode.com/2024/day/[x]

# find part 1 at ./part1.py
# find part 2 at ./part2.py

filename = ["sample1.txt", "input.txt"][0]

with open(filename, "r") as reader:
    for line in reader.readlines():
        print(line, end="")
