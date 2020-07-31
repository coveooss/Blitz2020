import logging
import uuid
from abc import ABC, abstractmethod

from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState


class AbstractViewer(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger("AbstractViewer")
        self.uid = str(uuid.uuid4())

    async def close(self) -> None:
        pass

    @abstractmethod
    async def send_tick(self, game_tick: int, game_state: GameState) -> None:
        pass

    @abstractmethod
    async def send_winner(self, game_tick: int, player_state: PlayerState) -> None:
        pass
