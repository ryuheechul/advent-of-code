# https://adventofcode.com/2024/day/6


from enum import Enum, auto
from typing import Iterable


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

    def __init__(self, grid: list[list[Mark]]) -> None:
        self.coords, self.current = find_started(grid)
        self.grid = grid

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

        # here is where i should try and catch (that means it leaves the grid)

        try:
            if self.grid[y][x] == Mark.Obstacle:
                return False
        except Exception:
            return True  # delegate the handling of exception at the caller

        return True

    def forward(self):
        if not self.can_forward():
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

    def debug_print(self):
        for line in ([convert_to_sign(mark) for mark in line] for line in self.grid):
            print("".join(line))
        print()

    def turn(self):
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


with open("input.txt", "r") as reader:
    parsed_grid = parse(list(line.strip()) for line in reader.readlines())

    guard = Guard(parsed_grid)

    result = guard.play()

    print(result)
