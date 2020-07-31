import logging
from abc import ABC, abstractmethod

from blitz2020.game.game import Game
from blitz2020.game.game_config import GameConfig
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState


class AbstractServer(ABC):
    def __init__(self, max_nb_ticks: int, game_config: GameConfig = None, game_delay: int = 0, move_timeout: int = 1):
        self.logger = logging.getLogger("AbstractServer")

        if game_config is not None:
            self.game_map: GameMap = game_config.game_map
            self.game_state: GameState = GameState(game_config)
        else:
            self.game_map = GameMap(25)
            self.game_state = GameState(self.game_map)

        self.game: Game = Game(self.game_state, max_nb_ticks=max_nb_ticks, delay=game_delay, move_timeout=move_timeout)

    @abstractmethod
    async def start(self) -> bool:
        pass
