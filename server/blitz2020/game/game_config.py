from os import PathLike
from typing import List

from blitz2020.game.direction import Direction
from blitz2020.game.game_map import GameMap
from blitz2020.game.position import Position


class GameConfig:
    def __init__(self, game_map: GameMap, spawn_positions: List[Position], spawn_directions: List[Direction] = None):
        self.game_map = game_map
        self.spawn_positions = spawn_positions
        self.spawn_directions = spawn_directions

    @classmethod
    def from_str(cls, data: str) -> "GameConfig":
        lines = data.strip().split("\n")

        map_size = len(lines)
        game_map = GameMap(map_size)

        spawn_positions = []
        spawn_directions = []
        spawn_direction_markers = []

        for y, line in enumerate(lines):
            line = line.strip()
            if len(line) != map_size:
                raise Exception(f"Map is not square! (line {y} as length {len(line)})")

            for x, tile in enumerate(line):
                pos = Position(x, y)
                if tile == GameMap.EMPTY:
                    game_map.set_tile(pos, GameMap.EMPTY, None)
                elif tile == GameMap.ASTEROIDS:
                    game_map.set_tile(pos, GameMap.ASTEROIDS, None)
                elif tile == GameMap.BLACK_HOLE:
                    game_map.set_tile(pos, GameMap.BLACK_HOLE, None)
                elif tile == GameMap.BLITZIUM:
                    game_map.set_tile(pos, GameMap.BLITZIUM, None)
                elif tile == GameMap.PLANET:
                    game_map.set_tile(pos, GameMap.PLANET, None)
                elif tile == GameMap.DIRECTION:
                    # Directions are meta information not visible on the map
                    game_map.set_tile(pos, GameMap.EMPTY, None)
                    spawn_direction_markers.append(pos)
                elif tile.isdigit():
                    player_id = int(tile)
                    spawn_positions.append((player_id, pos))
                else:
                    raise Exception(f"Invalid tile '{tile}' as position {pos}.")

        spawn_positions.sort()

        if len(spawn_direction_markers) > 0:
            # for each player we find the closest direction marker
            # this algorithm won't work if a direction marker is
            # close to 2 spawn_positions
            for player_id, spawn_position in spawn_positions:
                for direction_marker in spawn_direction_markers:
                    if spawn_position.is_next_to(direction_marker):
                        direction = spawn_position.direction_to(direction_marker)
                        spawn_directions.append(direction)

        return GameConfig(game_map, [p for i, p in spawn_positions], spawn_directions)

    @classmethod
    def from_file(cls, path: PathLike) -> 'GameConfig':
        with open(path) as f:
            data = f.read()
            return GameConfig.from_str(data)
