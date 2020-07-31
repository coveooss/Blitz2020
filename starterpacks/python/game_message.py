from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
from typing import List, Dict


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class TileType(Enum):
    EMPTY = " "
    ASTEROIDS = "W"
    PLANET = "%"
    BLITZIUM = "$"
    BLACK_HOLE = "!"
    CONQUERED = "C-"
    CONQUERED_PLANET = "%-"

    @staticmethod
    def get_tile_type(raw_tile: str) -> 'TileType':
        for tile_type in TileType:
            if raw_tile == tile_type.value:
                return tile_type
        if raw_tile.startswith(TileType.CONQUERED.value):
            return TileType.CONQUERED
        elif raw_tile.startswith(TileType.CONQUERED_PLANET.value):
            return TileType.CONQUERED_PLANET
        else:
            raise Exception(f"Tile '{raw_tile}'' is not a valid tile.")


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Game:
    pretty_map: str
    map: List[List[str]]
    tick: int
    ticks_left: int
    player_id: int

    def _validate_tile_exists(self, point: Point):
        if point.y < 0 or not point.y < len(self.map):
            raise Exception(f"y: '{point.y}' is out of bounds. Max y is {len(self.map) - 1}.")
        if point.x < 0 or not point.x < len(self.map):
            raise Exception(f"x: '{point.x}' is out of bounds. Max x is {len(self.map) - 1}.")

    def get_tile_owner_id(self, point: Point) -> int:
        self._validate_tile_exists(point)

        tile = self.map[point.y][point.x]
        if "-" not in tile:
            raise Exception(f"The tile at y: '{point.y}', x: '{point.x} is not captured.'")

        return int(tile[-1])

    def get_tile_type_at(self, point: Point) -> TileType:
        self._validate_tile_exists(point)

        return TileType.get_tile_type(self.map[point.y][point.x])


@dataclass
class Turn:
    tick: int
    message: str


@dataclass
class Player:
    id: int
    name: str
    score: float
    active: bool
    killed: bool
    position: Point
    spawn_position: Point
    direction: Direction
    tail: List[Point] = field(default_factory=lambda: [])
    history: List[Turn] = field(default_factory=lambda: [])


@dataclass_json
@dataclass
class GameMessage:
    type: str
    game: Game
    players: List[Player]

    def generate_players_by_id_dict(self) -> Dict[int, Player]:
        return {player.id: player for player in self.players}
