# https://adventofcode.com/2024/day/6


import copy
from enum import Enum, auto
from typing import Iterable


class LoopDetected(Exception):
    pass


class Mark(Enum):
    Free = 0
    Obstacle = auto()
    Been = auto()
    ToNorth = auto()
    ToEast = auto()
    ToSouth = auto()
    ToWest = auto()

    def score(self):
        try:
            return {
                mark: False
                for mark in [
                    Mark.Obstacle,
                    Mark.Free,
                ]
            }[self]
        except Exception:
            return True


def find_started(grid: list[list[Mark]]):
    for y, line in enumerate(grid):
        for x, mark in enumerate(line):
            if mark in [Mark.ToEast, Mark.ToNorth, Mark.ToWest, Mark.ToSouth]:
                return (x, y), mark

    raise ValueError("Could't find starting position")


class Guard:
    coords = (0, 0)
    grid: list[list[Mark]]
    current = Mark.ToNorth
    left = False
    # e.g. { ((2,0), Mark.ToNorth), ((8,1), Mark.ToNorth), ((7,4), Mark.ToNorth), ((1,3), Mark.ToNorth) }
    # ```
    # ..#.....
    # ..^>>>>>#
    # ..^....V
    # .#<<<<<V
    # .......O
    # ````
    # any of them will hit again but `((2,0), Mark.ToNorth)` will be first to hit again
    loop_bucket: set[tuple[tuple[int, int], Mark]]
    # loop_bucket: set[tuple[int, int]]

    def __init__(self, grid: list[list[Mark]]) -> None:
        self.coords, self.current = find_started(grid)
        self.grid = grid
        self.loop_bucket = set()

    def at_next(self):
        match self.current:
            case Mark.ToNorth:
                d_x, d_y = 0, -1
            case Mark.ToEast:
                d_x, d_y = 1, 0
            case Mark.ToSouth:
                d_x, d_y = 0, 1
            case Mark.ToWest:
                d_x, d_y = -1, 0
            case _:
                raise ValueError(
                    f"this can't be possible - self.current: {self.current}"
                )

        x, y = self.coords
        new_coords = x + d_x, y + d_y
        return new_coords

    def can_forward(self):
        x, y = self.at_next()

        # not having the condition below cost me so much time on even though I was pretty close! - you can see that without this, part 1 worked fine by comparing with ./part1.py
        # but thanks to `./sample3.txt`, I was able to tell what was going bad
        if x < 0 or y < 0:
            return True  # can forward for the exit

        # here is where i should try and catch (that means it leaves the grid)

        try:
            if self.grid[y][x] == Mark.Obstacle:
                return False
        except Exception:
            return True  # delegate the handling of exception at the caller

        return True

    def forward(self):
        while not self.can_forward():
            self.turn()

        new_coords = self.at_next()
        ox, oy = self.coords

        self.grid[oy][ox] = Mark.Been

        x, y = new_coords

        # INFO: due to python's convenient negative index which is bug inducing in this case;
        # have to block this manually - otherwise it will jump on to the other side!
        # discovered this thanks to observing the "animation" via `self.debug_print()`
        if x < 0 or y < 0:
            self.left = True
            return

        # just to be cautious in case I didn't do it right
        if (
            y > 0
            and x > 0
            and y < len(self.grid)
            and x < len(self.grid[0])
            and self.grid[y][x] == Mark.Obstacle
        ):
            self.debug_print()
            raise ValueError("Something went wrong!")

        # taking care of positive indexing error with try catch
        try:
            self.grid[y][x] = self.current
            self.coords = new_coords
        # means it's game over now
        except Exception:
            # restore for debugging purpose
            self.grid[oy][ox] = self.current
            self.left = True

    def count(self):
        def count_line(li: list[Mark]):
            return sum(mark.score() for mark in li)

        return sum(count_line(line) for line in self.grid)

    def play(self):
        # self.debug_print()
        while not self.left:
            self.forward()
            # self.debug_print()

        # self.debug_print()
        return self.count()

    def detect_loop(self):
        try:
            # self.debug_print()
            while not self.left:
                self.forward()
                # self.debug_print()

            # self.debug_print()
            return False
        except LoopDetected:
            # print(self.loop_bucket)
            # self.debug_print()
            return True
        except Exception as e:
            raise e

    def debug_print(self):
        for line in ([convert_to_sign(mark) for mark in line] for line in self.grid):
            print("".join(line))
        print()

    def try_detect(self):
        to_save = (self.coords, self.current)
        if to_save in self.loop_bucket:
            raise LoopDetected(f"loop detected at ({self.current})")

        self.loop_bucket.add(to_save)

    def turn(self):
        self.try_detect()

        self.current = self.new_direction()

    def new_direction(self):
        match self.current:
            case Mark.ToNorth:
                return Mark.ToEast
            case Mark.ToEast:
                return Mark.ToSouth
            case Mark.ToSouth:
                return Mark.ToWest
            case Mark.ToWest:
                return Mark.ToNorth
            case _:
                raise ValueError(f"{self.current} can't tell you the next direction")


def convert_to_sign(mark: Mark):
    match mark:
        case Mark.Obstacle:
            return "#"
        case Mark.Free:
            return "."
        case Mark.Been:
            return "X"
        case Mark.ToNorth:
            return "^"
        case Mark.ToEast:
            return ">"
        case Mark.ToSouth:
            return "V"
        case Mark.ToWest:
            return "<"


def convert_to_mark(sign: str):
    match sign:
        case "#":
            return Mark.Obstacle
        case ".":
            return Mark.Free
        case "^":
            return Mark.ToNorth
        case ">":
            return Mark.ToEast
        case "V":
            return Mark.ToSouth
        case "<":
            return Mark.ToWest
        case "X":
            return Mark.Been
        case s:
            raise ValueError(f"{s} was not expected")


def convert_to_marks(signs: list[str]):
    return [convert_to_mark(sign) for sign in signs]


def parse(li: Iterable[list[str]]):
    return [convert_to_marks(line) for line in li]


def mark_deadzones(grid: list[list[Mark]]):
    played = Guard(copy.deepcopy(grid))
    # played.debug_print()
    played.play()
    # played.debug_print()

    deadzone_grid = [
        [False for _ in range(0, len(grid[0]))] for _ in range(0, len(grid))
    ]

    if len(deadzone_grid) != len(grid) or len(deadzone_grid[0]) != len(grid[0]):
        raise ValueError("found yourself a situation")

    for y, line in enumerate(played.grid):
        for x, mark in enumerate(line):
            if mark == Mark.Free:
                # to include 8 surround marks safely
                to_find_any_beens = set()

                if y > 0:
                    to_find_any_beens.add((x, y - 1))
                if x > 0:
                    to_find_any_beens.add((x - 1, y))

                if y < len(deadzone_grid):
                    to_find_any_beens.add((x, y + 1))
                if x < len(line):
                    to_find_any_beens.add((x + 1, y))

                if y > 0 and x > 0:
                    to_find_any_beens.add((x - 1, y - 1))
                if y > 0 and x > len(line):
                    to_find_any_beens.add((x + 1, y - 1))

                if y < len(deadzone_grid) and x > 0:
                    to_find_any_beens.add((x - 1, y + 1))
                if y < len(deadzone_grid) and x < len(line):
                    to_find_any_beens.add((x + 1, y + 1))

                # not worth investigating if there is no trace of walked path
                if sum(m == Mark.Been for m in to_find_any_beens) == 0:
                    deadzone_grid[y][x] = True

    return deadzone_grid


def gen_loops(grid: list[list[Mark]]):
    deadzones = mark_deadzones(grid)

    for y, line in enumerate(grid):
        for x, mark in enumerate(line):
            if mark == Mark.Free and not deadzones[y][x]:
                new_grid = copy.deepcopy(grid)
                new_grid[y][x] = Mark.Obstacle
                yield new_grid


# thanks https://www.reddit.com/r/adventofcode/comments/1h8e0fs/comment/m0s7egy/ for ./sample2.txt
# thanks https://www.reddit.com/r/adventofcode/comments/1h8in8j/comment/m0t7mlt/ for ./sample3.txt

with open("input.txt", "r") as reader:
    parsed_grid = parse(list(line.strip()) for line in reader.readlines())

    s = sum(Guard(modified).detect_loop() for modified in gen_loops(parsed_grid))

    print(s)


# How do I detect the loop?
# - obstacle being touched from the same direction twice means there is a loop somewhere whether it's a square or more complicated structure
# - be careful with negative index... it bit me hard twice
# - using pypy was 10 times faster
# - I saved even more time by opt out of the spots were never visited by regular traverse
# - took about 10 seconds with pypy and skipping deadzones, 40 seconds for brute force, 10x more in case with cpython instead pypy
#   - this can be further improved by employing multiprocessing but I'm not gonna bother as 10~ seconds for this is acceptable for me
