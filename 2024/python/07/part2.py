# https://adventofcode.com/2024/day/7

from enum import Enum, auto
import itertools


class Operator(Enum):
    Add = 0
    Multiply = auto()
    Glue = auto()


def operator_sets(repeat: int):
    return itertools.product(
        [Operator.Add, Operator.Multiply, Operator.Glue], repeat=repeat
    )


def glue(left: int, right: int):
    m = float(right)
    digit_count = 1
    while m >= 10:
        m = m / 10
        digit_count += 1
    return 10**digit_count * left + right


def operate(left: int, right: int, op: Operator) -> int:
    return {
        Operator.Add: lambda: left + right,
        Operator.Multiply: lambda: left * right,
        # Operator.Glue: lambda: int(str(left) + str(right)),
        Operator.Glue: lambda: glue(left, right),  # ever so slightly faster than above
    }[op]()


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
    ops_sets = list(operator_sets(len(atoms) - 1))

    return expected if any(verify_set(expected, atoms, ops) for ops in ops_sets) else 0


with open("input.txt", "r") as reader:
    # ~30 seconds with pypy
    # ~275 seconds with cpython
    s = sum(verify(*parse(line)) for line in reader.readlines())

    print(s)

    ########
    # # below is same as the commented above but using multiprocessing
    # from multiprocessing import Pool
    #
    # def _verify(line: str):
    #     return verify(*parse(line))
    #
    # # ~40 seconds with pypy - why the heck is slower than single processing above?
    # # ~365 seconds with cpython
    # # these performance issue gets worse with more pool count
    # with Pool(4) as p:
    #     s = sum(p.imap_unordered(_verify, (line for line in reader.readlines())))
    #     print(s)

    ########
    # # similar speed to single process (slightly slower)
    # from multiprocessing.dummy import Pool as ThreadPool
    #
    # def _verify(line: str):
    #     return verify(*parse(line))
    #
    # with ThreadPool() as p:
    #     # results = pool.map(my_function, my_array)
    #     s = sum(p.starmap(_verify, [line for line in reader.readlines()]))
    #     print(s)
