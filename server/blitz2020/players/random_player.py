import logging
import random
from typing import Tuple, Optional

from blitz2020.game.abstract_player import AbstractPlayer
from blitz2020.game.action import Action
from blitz2020.game.game_state import GameState


class RandomPlayer(AbstractPlayer):
    def __init__(self, name: str = "random-player") -> None:
        super().__init__(name)
        self.logger = logging.getLogger("RandomPlayer")

    async def request_next_move_impl(self, game_tick: int, game_state: GameState) -> Tuple[Optional[int], Action]:
        self.logger.info(f"{self.name_str()}: game_tick={game_tick}")
        return game_tick, random.choice([Action.FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT])
