from typing import List

from blitz2020.game.game_map import GameMap
from blitz2020.game.position import Position

P = -3
W = -2
E = -1
P1 = -4


def create_map_with(map_data: List[List[int]]) -> GameMap:
    data_size = len(map_data)
    assert data_size == len(map_data[0])
    game_map = GameMap(data_size + 2)
    for y in range(data_size):
        for x in range(data_size):
            pos = Position(x + 1, y + 1)
            if map_data[y][x] == W:
                game_map.set_tile(pos, GameMap.ASTEROIDS, player_id=None)
            elif map_data[y][x] == E:
                game_map.set_tile(pos, GameMap.EMPTY, player_id=None)
            elif map_data[y][x] == P:
                game_map.set_tile(pos, GameMap.PLANET, player_id=None)
            elif map_data[y][x] == P1:
                game_map.set_tile(pos, GameMap.PLANET, player_id=1)
            else:
                game_map.conquer_tile(pos, player_id=map_data[y][x])
    return game_map
