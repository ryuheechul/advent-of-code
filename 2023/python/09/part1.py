# https://adventofcode.com/2023/day/9


def parse():
    with open("input.txt", "r") as reader:
        sequences = [list(map(int, line.split())) for line in reader.readlines()]

        return sequences


def calc_diffs(seq: list[int]):
    lefty = seq[0:-1]
    righty = seq[1:]

    return [r - l for l, r in zip(lefty, righty)]


def predict(seq: list[int]):
    last = seq[-1]
    diffs = calc_diffs(seq)

    is_all_0 = all(diff == 0 for diff in diffs)

    if is_all_0:
        return last

    return last + predict(diffs)


if __name__ == "__main__":
    seqs = parse()

    answer = sum(predict(s) for s in seqs)

    print(answer)
