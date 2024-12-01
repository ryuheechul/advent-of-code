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
    left, right = _left, list(_right)

    similarity_sum = sum(right.count(n) * n for n in left)
    print(similarity_sum)
