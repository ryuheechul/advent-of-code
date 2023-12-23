# https://adventofcode.com/2023/day/5

with open("input.txt", "r") as reader:
    firstline = reader.readline()
    _, _seeds = firstline.split(": ", 2)
    seeds = [int(seed) for seed in _seeds.split()]

    hold = seeds
    bucket: dict[int, int | None] = dict((s, None) for s in range(len(hold)))

    for line in reader.readlines():
        if len(line) < 2:
            continue

        if not line[0].isdigit():
            # flush
            hold = [v if v else hold[idx] for idx, v in bucket.items()]
            bucket = dict((s, None) for s in range(len(hold)))
        else:
            dest, source, length = (int(s) for s in line.split(None, 3))

            # map with the special range
            for idx, item in enumerate(hold):
                if item in range(source, source + length):
                    bucket[idx] = dest - source + item

    # final flush
    hold = [v if v else hold[idx] for idx, v in bucket.items()]

    answer = min(hold)
    print(answer)
