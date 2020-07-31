from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import Optional, Deque, List, Dict

from blitz2020.game.game_map import GameMap
from blitz2020.game.player_stats import PlayerStats
from blitz2020.game.position import Direction
from blitz2020.game.position import Position


class HistoryItem:
    def __init__(self, game_tick: int, message: str, ts: Optional[datetime] = None) -> None:
        if ts:
            self.ts = ts
        else:
            self.ts = datetime.now()
        self.tick = game_tick
        self.message = message

    def __str__(self) -> str:
        return f"{self.ts} - Tick: {self.tick} - {self.message}"


class PlayerState:
    def __init__(
        self,
        id: int,
        name: str,
        game_map: GameMap,
        position: Optional[Position] = None,
        direction: Optional[Direction] = None,
        init: bool = True,
    ) -> None:
        self.id: int = id
        self.name = name
        self.game_map = game_map

        self.active = True  # True if the player is still playing
        self.killed = False  # When killed, player need to respawn
        self.score = 0.0
        self.stats: PlayerStats = PlayerStats()
        self.max_ticks_in_history = 10
        self.history: Deque[HistoryItem] = deque()

        self.spawn_position: Position = position or self.game_map.get_random_empty_position()
        self.position: Optional[Position] = None

        self.spawn_direction: Direction = direction or dir_to_center(self.spawn_position, self.game_map.size)
        self.direction: Optional[Direction] = None

        self.tail: List[Position] = []
        if init:
            self.reset_position()

    def __deepcopy__(self, memodict: Dict) -> PlayerState:
        gm = memodict[id(self.game_map)]
        obj = type(self)(self.id, self.name, gm, self.spawn_position.copy(), self.spawn_direction.copy(), init=False)
        obj.active = self.active
        obj.killed = self.killed
        obj.score = self.score
        if self.position:
            obj.position = self.position.copy()
        if self.direction:
            obj.direction = self.direction.copy()
        obj.tail = self.tail.copy()
        obj.stats = PlayerStats(self.stats.stats.copy(), self.stats.kills.copy(), self.stats.killed_by_players.copy())
        obj.max_ticks_in_history = 0
        return obj

    def name_str(self) -> str:
        return f"{self.name}-{self.id}"

    def __str__(self) -> str:
        tail_str = ", ".join([str(x) for x in self.tail])
        return f"['{self.name_str()}': Active: {self.active}, Killed: {self.killed}, Score: {self.score:.2f}, Position {self.position}, Direction: {self.direction}, Tail: [{tail_str}]], Stats: {self.stats}"

    def short_str(self) -> str:
        tail_str = ", ".join([str(x) for x in self.tail])
        return f"['{self.name_str()}': Score: {self.score:.2f}, Position {self.position}, Direction: {self.direction}, Tail: [{tail_str}]]"

    def reset_position(self) -> None:
        self.direction = self.spawn_direction.copy()
        self.position = self.spawn_position.copy()
        self.tail = [self.position.copy()]
        self.game_map.conquer_tile(self.position, self.id)
        self.stats.set_stat(PlayerStats.CONQUERED, 1)

    def add_history(self, game_tick: int, message: str) -> None:
        if self.max_ticks_in_history > 0:
            self.history.appendleft(HistoryItem(game_tick, message))
            game_tick_cutoff = game_tick - self.max_ticks_in_history
            while self.history[-1].tick < game_tick_cutoff:
                self.history.pop()

    def conquered_tiles(self) -> int:
        tiles = 0
        if PlayerStats.CONQUERED in self.stats.stats:
            tiles = self.stats.stats[PlayerStats.CONQUERED]
        return tiles


def dir_to_center(position: Position, map_size: int) -> Direction:
    # find the direction to the center of the map
    center_map = map_size / 2.0
    dx = position.x - center_map
    dy = position.y - center_map

    if abs(dx) <= abs(dy):
        # center is closer in the horizontal direction
        if dx < 0:
            dir = Direction.RIGHT
        else:
            dir = Direction.LEFT
    else:
        # center is closer in the vertical direction
        if dy < 0:
            dir = Direction.DOWN
        else:
            dir = Direction.UP

    return Direction(dir)
