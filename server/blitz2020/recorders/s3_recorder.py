import gzip
import json
import logging
from typing import List, Dict, Any

import boto3
from blitz2020.game.abstract_recorder import AbstractRecorder
from blitz2020.game.game import Game
from blitz2020.game.game_state import GameState
from blitz2020.servers.socket.utils import game_state_to_dict


class S3Recorder(AbstractRecorder):
    def __init__(self, game: Game, s3_bucket: str, s3_path: str, log_file: str):
        super().__init__()
        self.logger = logging.getLogger("S3 Recorder")

        self.s3 = boto3.resource("s3").Bucket(s3_bucket)
        self.s3_path = s3_path

        self.game = game
        self.ticks: List[Dict] = list()
        self.s3_path = s3_path
        self.log_file = log_file

    def close(self) -> None:
        sortedPlayersByScore = sorted(self.game.players, key=lambda p: p.player_state.score, reverse=True)

        gameResult = [
            {
                "teamId": player.uid,
                "teamName": player.name,
                "rank": sortedPlayersByScore.index(player) + 1,
                "score": player.player_state.score,
                "didTimeout": not player.player_state.active,
            }
            for player in self.game.players
        ]

        replay = {"ticks": self.ticks}

        self.upload_data_to_S3(gameResult, "gameResults.json")
        self.gzip_and_upload_data_to_S3(replay, "replay.gz")
        if self.log_file:
            logging.info("Uploading log file to s3, following logs will be in cloudwatch only")
            self.upload_file_to_S3(self.log_file, self.log_file)

    def record_tick(self, game_tick: int, game_state: GameState) -> None:
        self.logger.debug(f"{self.uid}: game_tick={game_tick}")

        tick = game_state_to_dict(
            game_tick, -1, game_state, ticks_left=self.game.max_nb_ticks - game_tick, with_history=False
        )
        self.ticks.append(tick)

    def upload_data_to_S3(self, data: Any, s3_file_name: str) -> None:
        self.s3.Object(key=self.s3_path + s3_file_name).put(Body=json.dumps(data))
        logging.info('Uploaded file "%s"', s3_file_name)

    def upload_file_to_S3(self, file_name: str, s3_file_name: str) -> None:
        self.s3.Object(key=self.s3_path + s3_file_name).upload_file(file_name)
        logging.info('Uploaded file "%s"', s3_file_name)

    def gzip_and_upload_data_to_S3(self, data: Any, s3_file_name: str) -> None:
        with gzip.open(s3_file_name, "wt", encoding="utf8") as f:
            json.dump(data, f)

        self.s3.Object(key=self.s3_path + s3_file_name).upload_file(s3_file_name)
        logging.info('Uploaded file "%s"', s3_file_name)
