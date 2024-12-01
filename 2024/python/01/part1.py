# https://adventofcode.com/2024/day/01


with open("input.txt", "r") as reader:
    _left, _right = zip(
        *(
            (int(chunk[0]), int(chunk[-1]))
            for chunk in (
                line.strip().split() for line in reader.readlines() if len(line.strip())
            )
        )
    )
    left, right = sorted(_left), sorted(_right)
    zipped = zip(left, right)

    diff_sum = sum(abs(left - right) for left, right in zipped)
    print(diff_sum)
