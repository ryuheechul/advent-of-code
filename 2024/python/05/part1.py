# https://adventofcode.com/2024/day/5

rules = []
events = []

is_time_to_update = False


def parse_rule(line: str):
    left, right = line.strip().split("|", 1)

    rules.append((int(left), int(right)))


def parse_update_event(line: str):
    events.append([int(s) for s in line.strip().split(",")])


def verify_rule(rule: tuple[int, int], page: int, pages: list[int]):
    if page not in rule:
        return True

    left, right = rule

    if left not in pages or right not in pages:
        return True

    return pages.index(left) < pages.index(right)


def verify_page(page: int, pages: list[int]):
    return sum(verify_rule(rule, page, pages) for rule in rules) == len(rules)


def mid_index(li: list):
    # 0   1   2   [3]
    #       len-1 len
    #     x

    # 0   1   2   3   4   5   6   [7]
    #                       len-1 len
    #             x
    return int((len(li) - 1) / 2)

def verify_event(pages: list[int]):
    for page in pages:
        if not verify_page(page, pages):
            return 0

    return pages[mid_index(pages)]


with open("input.txt", "r") as reader:
    for line in reader.readlines():
        if is_time_to_update:
            parse_update_event(line)
        else:
            if not len(line.strip()):
                is_time_to_update = True
                continue

            parse_rule(line)

    s = sum(verify_event(pages) for pages in events)
    print(s)
