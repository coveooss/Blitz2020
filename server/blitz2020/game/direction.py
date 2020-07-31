from typing import Dict, Tuple, Union, List

from blitz2020.game.action import Action


class Direction:
    """
    A class used to represent a direction.

    top-left is 0-0
    x: horizontal axis
    y: vertical axis

    """

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(self, direction: Union['Direction', Tuple[int, int], str]):
        if isinstance(direction, Direction):
            self.dir: int = direction.dir
        elif isinstance(direction, tuple) and direction in inv_direction_delta:
            self.dir = inv_direction_delta[direction]
        elif isinstance(direction, str) and direction in inv_direction_str:
            self.dir = inv_direction_str[direction]
        else:
            msg = f"Invalid argument: '{direction}'"
            raise Exception(msg)

    def dx(self) -> int:
        return self.delta()[0]

    def dy(self) -> int:
        return self.delta()[1]

    def delta(self) -> Tuple[int, int]:
        return directions[self.dir][1]

    def name(self) -> str:
        return self.to_string()

    def change_direction(self, action: Action) -> "Direction":
        """
        Apply action and change direction

        Parameters
        ----------
        action : player action
        """
        delta = action_to_delta[action]
        self.dir = (self.dir + delta) % len(directions)

        return self

    def copy(self) -> "Direction":
        return Direction(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Direction):
            return self.dir == other.dir
        if isinstance(other, str):
            return directions[self.dir][0] == other
        return NotImplemented

    def to_string(self) -> str:
        return directions[self.dir][0]

    def __str__(self) -> str:
        return f"[{self.to_string()}, (dx: {self.dx()}, dy: {self.dy()})]"


directions: List[Tuple[str, Tuple[int, int]]] = [
    (Direction.UP, (0, -1)),
    (Direction.LEFT, (-1, 0)),
    (Direction.DOWN, (0, 1)),
    (Direction.RIGHT, (1, 0)),
]

inv_direction_str: Dict[str, int] = {k[0]: i for i, k in enumerate(directions)}

inv_direction_delta: Dict[Tuple[int, int], int] = {k[1]: i for i, k in enumerate(directions)}

action_to_delta: Dict[Action, int] = {Action.FORWARD: 0, Action.TURN_LEFT: 1, Action.TURN_RIGHT: -1}
