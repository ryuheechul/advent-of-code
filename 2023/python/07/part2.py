# https://adventofcode.com/2023/day/7

from typing import Any

label_rank = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

# this just needs to be bigger than the biggest label rank which is 13
# otherwise some score will not represent clearly which order wins first
pow_base = 14

# types
# 1. Five of a kind, where all five cards have the same label: AAAAA
# 2. Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# 3. Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# 4. Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# 5. Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# 6. One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# 7. High card, where all cards' labels are distinct: 23456

# ts: type score
# 5 is chosen here since the biggest for label is 4
# but anything bigger than 4 should work

ts_multiplier = pow(pow_base, 5)

ts_5_of_a_kind = 7
ts_4_of_a_kind = 6
ts_full_house = 5
ts_3_of_a_kind = 4
ts_2_pair = 3
ts_1_pair = 2
ts_high_card = 1


def pick_best_to_use_joker_for(ledger: dict[str, int]):
    m = max(ledger.values())

    best = "J"  # start with the weakest
    for label, value in ledger.items():
        if value == m and label_rank[label] > label_rank[best]:
            best = label

    return best


def figure_type(hand: str):
    ledger = {}

    joker_count = 0
    for label in hand:
        if label == "J":
            joker_count += 1
            continue
        count = ledger.get(label, 0)
        count += 1
        ledger[label] = count

    # handle a edge case first
    if joker_count == 5:
        ledger["J"] = 5
    # and compensate the joker count
    elif joker_count > 0:
        l = pick_best_to_use_joker_for(ledger)
        ledger[l] += joker_count

    counts = ledger.values()

    ts = ts_high_card
    if 5 in counts:
        ts = ts_5_of_a_kind
    elif 4 in counts:
        ts = ts_4_of_a_kind
    elif 3 in counts and 2 in counts:
        ts = ts_full_house
    elif 3 in counts:
        ts = ts_3_of_a_kind
    elif list(counts).count(2) == 2:
        ts = ts_2_pair
    elif list(counts).count(2) == 1:
        ts = ts_1_pair

    return ts


def score_labels_in_hand(hand: str):
    return sum(
        pow(pow_base, idx) * label_rank[l] for idx, l in enumerate(reversed(hand))
    )


def parse_hand(line: str):
    hand, _bid = line.split(None, 2)
    bid = int(_bid)

    return hand, bid, figure_type(hand)


with open("input.txt", "r") as reader:
    hands = [parse_hand(line) for line in reader.readlines()]

    def sort_hands(h: tuple[str, int, Any]):
        hand, _, type_score = h

        label_order_score = score_labels_in_hand(hand)

        # making sure type_score_score has higher magnitude than label_order_score in any case
        type_score_score = type_score * ts_multiplier

        score = type_score_score + label_order_score
        return score

    distilled = (
        (idx + 1, bid) for idx, (_, bid, _) in enumerate(sorted(hands, key=sort_hands))
    )

    s = sum(rank * bid for rank, bid in distilled)

    print(s)
