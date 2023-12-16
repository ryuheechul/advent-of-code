# https://adventofcode.com/2023/day/3

def adjacents(y: int, x: int, length: int):
    "given y, x, length, return list of indices of adjacent cells"

    head = x - 1
    tail = length + 1

    return [
        (x_prime, y_prime)
        for y_prime in range(y-1, y+2)
        for x_prime in range(head, head + tail + 1)
    ]


def parse_number(line: str, x: int):
    '''
    given with the starting index of the first number, parse the whole number and return the information about the number
    e.g. the number, length
    '''

    length = 0

    to_be_n = ''

    for i in range(len(line) - x):
        target = line[x+i]
        if not is_number(target):
            break

        length += 1
        to_be_n += target

    n = 0 if len(to_be_n) == 0 else int(to_be_n)

    return n, length

def is_number(char: str):
    import re
    return re.match('[0-9]', char) is not None

def is_symbol(char: str):
    return char in [
        '!',
        '@',
        '#',
        '$',
        '%',
        '^',
        '&',
        '*',
        '-',
        '+',
        '=',
        '/',
    ]

def is_any_adjacent_symbol(map: list[str], candidates: list[tuple[int, int]], max_r: int, max_b: int):
    for candidate in candidates:
        x, y = candidate
        # `x >= max_r` is not necessary due to extra new line char at the end of each line
        if x < 0 or y < 0 or x > max_r or y >= max_b:
            continue

        if is_symbol(map[y][x]):
            return True

    return False


def collect_data():
    lines = []
    parsed_numbers = []
    with open('input.txt', 'r') as reader:
        y = 0
        for line in reader.readlines():
            lines.append(line)
            to_parse = 0
            for x, char in enumerate(line):
                if x != to_parse:
                    continue

                if is_number(char):
                    n, length = parse_number(line, x)
                    parsed_numbers.append((n, length, x, y))
                    to_parse += length
                else:
                    to_parse += 1
            y += 1

    return lines, parsed_numbers

lines, parsed_numbers = collect_data()
filtered = []
len_y = len(lines)
len_x = len(lines[0])

s = sum(
    n
    for n, length, x, y in parsed_numbers
    if is_any_adjacent_symbol(
        lines,
        adjacents(y, x, length),
        len_x,
        len_y
    )
)

print(s)
