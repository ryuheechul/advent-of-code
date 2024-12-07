# https://adventofcode.com/2024/day/7

from enum import Enum, auto
import itertools


class Operator(Enum):
    Add = 0
    Multiply = auto()


def operator_sets(repeat: int):
    return itertools.product([Operator.Add, Operator.Multiply], repeat=repeat)


def operate(left: int, right: int, op: Operator):
    return {
        Operator.Add: left + right,
        Operator.Multiply: left * right,
    }[op]


def parse(line: str):
    _expected, rest = line.strip().split(": ", 1)
    expected = int(_expected)

    atoms = [int(s) for s in rest.split()]

    return expected, atoms


def verify_set(expected: int, atoms: list[int], ops: tuple[Operator, ...]):
    iter_atoms = iter(atoms)
    acc = next(iter_atoms)

    for i, right in enumerate(iter_atoms):
        op = ops[i]
        acc = operate(acc, right, op)

    return expected == acc


def verify(expected: int, atoms: list[int]):
    ops_sets = operator_sets(len(atoms) - 1)

    return (
        expected if sum(verify_set(expected, atoms, ops) for ops in ops_sets) > 0 else 0
    )


with open("input.txt", "r") as reader:
    s = sum(verify(*parse(line)) for line in reader.readlines())

    print(s)
