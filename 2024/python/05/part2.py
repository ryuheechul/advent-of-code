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


def fix_by_rule(rule: tuple[int, int], pages: list[int]):
    left, right = rule

    # when nothing to fix
    if pages.index(left) < pages.index(right):
        return pages

    # with my current code, even without copy should just work but copying to be safe
    new_pages = pages.copy()

    # 0 1 r 3 l 5
    #
    #     |
    #     V
    #
    # 0 1 l 3 r 5
    new_pages[pages.index(right)] = left
    new_pages[pages.index(left)] = right

    return new_pages


def correct_update(pages: list[int]):
    for rule in rules:
        for page in pages:
            if not verify_rule(rule, page, pages):
                # until it correct all rules - it wouldn't work with any unfixable ones though
                return correct_update(fix_by_rule(rule, pages))

    return pages


def verify_event(pages: list[int]):
    is_correct = True
    for page in pages:
        if not verify_page(page, pages):
            is_correct = False
            break

    if is_correct:
        return 0

    corrected = correct_update(pages)
    return corrected[mid_index(corrected)]


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
