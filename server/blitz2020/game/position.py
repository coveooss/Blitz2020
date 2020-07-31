from __future__ import annotations

from typing import Tuple, Union, Optional

from blitz2020.game.direction import Direction


class Position:
    """
    A class used to represent a position on a map

    top-left is 0-0

    Attributes
    ----------
    x : int
        the horizontal axis (left-right)
    y : int
        the vertical axis (up-down)
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, other: Union[Direction, Tuple[int, int]]) -> Position:
        if isinstance(other, (tuple, list)):
            self.x += other[0]
            self.y += other[1]
        elif isinstance(other, Direction):
            self.x += other.dx()
            self.y += other.dy()
        else:
            raise Exception(f"Position: cannot move with {other}")

        return self

    def copy(self) -> Position:
        """
        Copy the current position into a new position
        """
        return Position(self.x, self.y)

    def is_next_to(self, other: Position) -> bool:
        return (self.y + 1 == other.y or self.y - 1 == other.y or self.x + 1 == other.x or self.x - 1 == other.x) and (
            self.x == other.x or self.y == other.y
        )

    def direction_to(self, target: Position) -> Optional[Direction]:
        if self.y > target.y:
            return Direction(Direction.UP)
        elif self.y < target.y:
            return Direction(Direction.DOWN)
        elif self.x > target.x:
            return Direction(Direction.LEFT)
        elif self.x < target.x:
            return Direction(Direction.RIGHT)
        else:
            return None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __str__(self) -> str:
        return f"[x: {self.x}, y: {self.y}]"

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)

    def __add__(self, other: Direction) -> Position:
        return self.copy().move(other)
