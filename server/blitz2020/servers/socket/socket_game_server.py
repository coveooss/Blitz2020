import asyncio
import json
import logging
from asyncio import Future
from typing import Dict, Optional, cast

import websockets
from websockets import WebSocketServer

from blitz2020.game.abstract_player import AbstractPlayer
from blitz2020.game.game_config import GameConfig
from blitz2020.recorders.json_recorder import JsonRecorder
from blitz2020.recorders.s3_recorder import S3Recorder
from blitz2020.servers.abstract_server import AbstractServer
from blitz2020.servers.socket.socket_player import SocketPlayer
from blitz2020.servers.socket.socket_viewer import SocketViewer


class SocketGameServer(AbstractServer):
    def __init__(
        self,
        max_nb_ticks: int = 1000,
        min_nb_players: int = 1,
        max_nb_players: int = 4,
        start_delay_timeout: int = 120,
        team_names_by_token: Dict[str, str] = None,
        game_config: GameConfig = None,
        path: str = "localhost",
        port: int = 8765,
        record_path: str = None,
        s3_bucket: str = None,
        s3_path: str = None,
        game_delay: int = 0,
        log_file: str = None,
        move_timeout: int = 1,
    ):
        super().__init__(max_nb_ticks, game_config, game_delay, move_timeout)
        self.logger = logging.getLogger("SocketGameServer")
        self.path = path
        self.port = port
        self.team_names_by_token = team_names_by_token
        self.game_loop_future: Optional[Future] = None
        self.auto_start_task: Optional[Future] = None
        self.server: Optional[WebSocketServer] = None

        # create json game recorder
        if record_path is not None:
            json_recorder = JsonRecorder(game=self.game, record_path=record_path)
            self.game.register_recorder(json_recorder)

        if s3_bucket is not None and s3_path is not None:
            s3_recorder = S3Recorder(game=self.game, s3_bucket=s3_bucket, s3_path=s3_path, log_file=log_file)
            self.game.register_recorder(s3_recorder)

        # Game options

        if team_names_by_token is not None:
            self.min_nb_players = len(team_names_by_token)
        else:
            self.min_nb_players = min_nb_players

        self.max_nb_players = max_nb_players
        if game_config and len(game_config.spawn_positions) > 0:
            self.max_nb_players = min(self.max_nb_players, len(game_config.spawn_positions))
        self.start_delay_timeout = start_delay_timeout

    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        message = await websocket.recv()
        try:
            data = json.loads(message)

            if data["type"] == "register":
                if self.team_names_by_token is not None:
                    if data["token"] and data["token"] in self.team_names_by_token:
                        await self.register_player(self.team_names_by_token[data["token"]], websocket)
                    else:
                        raise Exception(f"Invalid token received: '{data}'")
                else:
                    await self.register_player(data["name"], websocket)
            elif data["type"] == "viewer":
                await self.register_viewer(websocket)
            else:
                raise Exception(f"Invalid command received: '{data}'")
        except:
            self.logger.warning(f"Invalid message received: '{message!r}")

    async def register_player(self, player_name: str, websocket: websockets.WebSocketServerProtocol) -> None:
        self.logger.info(f"A new player just connected: '{player_name}'")

        if len(self.game.players) >= self.max_nb_players:
            self.logger.info(f"Player '{player_name}' refused, maximum number of player reached.")
        else:
            player = SocketPlayer(server=self, name=player_name, websocket=websocket)
            self.game.register_player(player)

            # if enough players, start the game loop task
            if len(self.game.players) >= self.min_nb_players and not self.game.is_started:
                self.logger.info("Enough players... Starting game.")

                # Let's cancel the scheduled auto start task if needed
                if self.auto_start_task is not None:
                    self.logger.debug("Cancelling the auto start task")
                    self.auto_start_task.cancel()

                self.auto_start_task.cancel()
                self.game_loop_future.set_result(asyncio.create_task(self.game.game_loop()))

            await self.wait_for_game_to_finish()

    async def register_viewer(self, websocket: websockets.WebSocketServerProtocol) -> None:
        viewer = SocketViewer(self, websocket=websocket)
        self.logger.info(f"A new viewer just joined: '{viewer.uid}'")
        self.game.register_viewer(viewer)
        await self.wait_for_game_to_finish()

    async def schedule_start_game(self) -> None:
        await asyncio.sleep(self.start_delay_timeout)

        if len(self.game.players) > 0:
            self.logger.info("Not all players registered correctly, starting game anyway.")
            self.game_loop_future.set_result(asyncio.create_task(self.game.game_loop()))

            await self.wait_for_game_to_finish()
        else:
            self.logger.info("No player registered in given start delay. Bye Bye.")
            self.game_loop_future.set_result(asyncio.create_task(self.start_timeout()))

    async def start_timeout(self) -> str:
        return "Timeout: No player registered"

    async def start(self) -> bool:
        self.logger.info(f"Starting game server on socket '{self.path}:{self.port}'")
        try:
            # receive the game loop task when enough players and the game is started
            self.game_loop_future = asyncio.get_running_loop().create_future()

            # game will start after start delay timeout if all players are not registered
            self.auto_start_task = asyncio.get_running_loop().create_task(self.schedule_start_game())

            # start socket server
            self.server = await websockets.serve(self.handle_message, self.path, self.port)

            return True

        except Exception as e:
            self.logger.critical(f"An error occurred while starting the server: {e}")
            return False

    async def wait_for_game_to_finish(self) -> AbstractPlayer:
        # wait until the game is started
        game = await self.game_loop_future
        # wait for the game to complete
        winner = await game
        return cast(AbstractPlayer, winner)

    async def terminate(self) -> None:
        # close the socket
        self.server.close()
        await self.server.wait_closed()
