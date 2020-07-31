import logging
import uuid
from abc import ABC, abstractmethod

from blitz2020.game.game_state import GameState


class AbstractRecorder(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger("AbstractRecorder")
        self.uid = str(uuid.uuid4())

    async def close(self) -> None:
        pass

    @abstractmethod
    def record_tick(self, game_tick: int, game_state: GameState) -> None:
        pass
