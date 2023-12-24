# https://adventofcode.com/2023/day/6


def count_winning_permutations(time: int, distance: int):
    return len([speed for speed in range(1, time) if speed * (time - speed) > distance])


def extract_time_distance_pairs():
    with open("input.txt", "r") as reader:
        time, distance = [
            map(
                int,
                line.split(": ", 2)[1].split(),
            )
            for line in reader.readlines()
        ]

        return list(zip(time, distance))


if __name__ == "__main__":
    pairs = extract_time_distance_pairs()

    import math

    answer = math.prod(count_winning_permutations(*a) for a in pairs)

    print(answer)
