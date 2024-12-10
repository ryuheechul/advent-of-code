# https://adventofcode.com/2024/day/[x]


filename = ["sample1.txt", "input.txt"][0]

with open(filename, "r") as reader:
    for line in reader.readlines():
        print(line, end="")
