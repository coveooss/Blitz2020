import logging
import uuid
from abc import ABC, abstractmethod
from typing import Tuple, Optional

from blitz2020.game.action import Action
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState


class AbstractPlayer(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.logger = logging.getLogger("AbstractPlayer")
        self.name = name
        self.uid = str(uuid.uuid4())
        self.player_state: Optional[PlayerState] = None

    def set_player_state(self, player_state: PlayerState) -> None:
        self.player_state = player_state
        self.logger.debug(f"set_player_state({self.name_str()})")

    def name_str(self) -> str:
        return self.player_state.name_str()

    async def close(self) -> None:
        pass

    async def request_next_move(self, game_tick: int, game_state: GameState) -> Tuple[Optional[int], Action]:
        self.logger.debug(f"{self.name_str()}: game_tick={game_tick}")
        tick, next_action = await self.request_next_move_impl(game_tick, game_state)
        self.logger.debug(f"{self.name_str()}: -> {next_action}")
        return tick, next_action

    @abstractmethod
    async def request_next_move_impl(self, game_tick: int, game_state: GameState) -> Tuple[Optional[int], Action]:
        pass
