import numpy as np

from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState
from blitz2020.game.position import Position

"""
  Map a game state to a frame

  empty: 0
  asteroids and blackholes: -1
  blitzium: 0.10
  planet: 0.25
  conquered by me = 0.75
  conquered by others = -0.10
  my head: 1
  my tail: 0.50
  other head: -0.75
  other tail: -0.5
"""

EMPTY = 0.0
ASTEROIDS_BH = -1.0
BLITZIUM = 0.10
PLANETS = 0.25
CAPTURED_BY_PLAYER = 1.0
CAPTURED_BY_OTHERS = -0.10
PLAYER_HEAD = 0.75
PLAYER_TAIL = 0.50
OTHERS_HEAD = -0.75
OTHERS_TAIL = -0.50


def payer_state_to_frame(player_state: PlayerState, frame, head: float, tail: float) -> np.array:
    for p in player_state.tail:
        frame[p.y, p.x] = tail
    frame[player_state.position.y, player_state.position.x] = head


def game_state_to_frame(player_id: int, state: GameState) -> np.array:
    size = state.game_map.size
    frame = np.zeros((size, size))

    for y in range(size):
        for x in range(size):
            tile_state, tile_owner = state.game_map.get_tile(Position(x, y))

            value = EMPTY
            if tile_state == GameMap.ASTEROIDS or tile_state == GameMap.BLACK_HOLE:
                value = ASTEROIDS_BH
            elif tile_state == GameMap.BLITZIUM:
                value = BLITZIUM
            elif tile_state == GameMap.PLANET and tile_owner != player_id:
                value = PLANETS

            if tile_owner is not None:
                if tile_owner == player_id:
                    value = CAPTURED_BY_PLAYER
                else:
                    value = CAPTURED_BY_OTHERS

            frame[y, x] = value

    for p in state.players:
        if p.id == player_id:
            payer_state_to_frame(p, frame, head=PLAYER_HEAD, tail=PLAYER_TAIL)
        else:
            payer_state_to_frame(p, frame, head=OTHERS_HEAD, tail=OTHERS_TAIL)

    return frame
