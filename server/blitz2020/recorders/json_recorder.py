import json
import logging
from typing import List, Dict

from blitz2020.game.abstract_recorder import AbstractRecorder
from blitz2020.game.game import Game
from blitz2020.game.game_state import GameState
from blitz2020.servers.socket.utils import game_state_to_dict


class JsonRecorder(AbstractRecorder):
    def __init__(self, game: Game, record_path: str, with_history: bool = False) -> None:
        super().__init__()
        self.logger = logging.getLogger("Recorder")
        self.game = game
        self.ticks: List[Dict] = list()
        self.record_path = record_path
        self.with_history = with_history

    def close(self) -> None:
        sortedPlayersByScore = sorted(self.game.players, key=lambda p: p.player_state.score, reverse=True)

        payload = {
            "ticks": self.ticks,
            "players": [player.player_state.name_str() for player in sortedPlayersByScore],
            "winner": sortedPlayersByScore[0].name,
        }

        with open(self.record_path, "w+") as file:
            file.write(json.dumps(payload, indent=2))

    def record_tick(self, game_tick: int, game_state: GameState) -> None:
        self.logger.debug(f"{self.uid}: game_tick={game_tick}")

        tick = game_state_to_dict(
            game_tick, -1, game_state, ticks_left=self.game.max_nb_ticks - game_tick, with_history=self.with_history
        )
        self.ticks.append(tick)
