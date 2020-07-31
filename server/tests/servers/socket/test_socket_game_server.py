import asyncio
import json
import logging
import unittest
from typing import List, Tuple, Optional

import websockets
from blitz2020.game.game_config import GameConfig
from blitz2020.servers.socket.socket_game_server import SocketGameServer
from tests.__main__ import enable_logging

path = "localhost"
port = 8765


class ReplaySocketPlayer:
    def __init__(self, name: str, actions: List[Tuple[float, str]]):
        self.name = name
        self.actions = actions
        self.logger = logging.getLogger("TestSocketPlayer")

    async def play(self):
        uri = f"ws://{path}:{port}"
        async with websockets.connect(uri) as websocket:
            try:
                for delay, action in self.actions:
                    self.logger.info(f"{self.name} [sleeping {delay}]'")
                    await asyncio.sleep(delay)

                    self.logger.info(f"{self.name} << '{action}'")
                    await websocket.send(action)

                    msg = await websocket.recv()
                    message = json.dumps(json.loads(msg), separators=(",", ":"))[:150] + "..."
                    self.logger.info(f"{self.name} >> '{message}'")

                    data = json.loads(msg)
                    if data["type"] != "tick":
                        raise Exception("Invalid tick")
            except Exception as e:
                self.logger.info(f"Got exception: {e}")


class ReplaySocketViewer:
    def __init__(self, name):
        self.logger = logging.getLogger("TestSocketViewer")
        self.name = name

    async def watch(self):
        uri = f"ws://{path}:{port}"
        async with websockets.connect(uri) as websocket:
            reg_str = '{ "type":"viewer" }'
            self.logger.info(f"{self.name} << '{reg_str}'")
            await websocket.send(reg_str)

            done = False
            while not done:
                msg = await websocket.recv()
                message = json.dumps(json.loads(msg), separators=(",", ":"))[:150] + "..."
                self.logger.info(f"{self.name} >> '{message}'")

                data = json.loads(msg)

                if data["type"] == "tick":
                    self.logger.info(f"{self.name} >> received tick: '{data['game']['tick']}'")
                elif data["type"] == "winner":
                    self.logger.info(f"{self.name} >> game done, winner: '{data['winner']}'")
                    done = True
                else:
                    raise Exception("Invalid action")


async def play_game(
    players: List[ReplaySocketPlayer], viewer: Optional[ReplaySocketViewer] = None, move_timeout=2.0, ticks=10
):
    server = SocketGameServer(max_nb_ticks=ticks, max_nb_players=2, path=path, port=port)
    server.game.move_timeout = move_timeout
    await server.start()

    if viewer:
        viewer_task = asyncio.create_task(viewer.watch())

    await asyncio.gather(*[player.play() for player in players])

    winner = await server.wait_for_game_to_finish()

    if viewer:
        await viewer_task

    await server.terminate()

    return winner, server.game


class TestSocketGameServer(unittest.TestCase):
    def test_simple_game(self):
        enable_logging(logging.INFO)
        self.logger = logging.getLogger("TestSocketGameServer")

        winner, game = asyncio.run(
            play_game(
                players=[
                    ReplaySocketPlayer(
                        "invalid", [(0, '{ "type":"xyz" }'), (0, '{ "type":"move", "action":"FORWARD" }')]
                    ),
                    ReplaySocketPlayer(
                        "mike",
                        [
                            (0, '{ "type":"register", "name":"mike" }'),
                            (0, '{ "type":"move", "action":"FORWARD" }'),
                            (0, '{ "type":"move", "action":"TURN_LEFT" }'),
                            (0, '{ "type":"move", "action":"TURN_RIGHT" }'),
                        ],
                    ),
                    ReplaySocketPlayer(
                        "jim",
                        [(0, '{ "type":"register", "name":"jim" }'), (0, '{ "type":"move", "action":"FORWARD" }')],
                    ),
                    ReplaySocketPlayer("too-late", [(0, '{ "type":"register", "name":"too-late" }')]),
                ],
                viewer=ReplaySocketViewer("viewer"),
                move_timeout=2,
                ticks=5,
            )
        )

        self.assertEqual(2, len(game.players))
        self.assertTrue(game.game_tick > 0)
        self.logger.info(winner.name_str())

    def test_player_with_slow_response_time(self):
        # enable_logging(logging.INFO)
        self.logger = logging.getLogger("TestSocketGameServer")

        ticks = 10
        timeout = 0.01
        winner, game = asyncio.run(
            play_game(
                players=[
                    ReplaySocketPlayer(
                        "mike",
                        [(0, '{ "type":"register", "name":"mike" }')]
                        + [(2 * timeout, '{ "type":"move", "action":"FORWARD" }') for i in range(2 * ticks)],
                    ),
                    ReplaySocketPlayer(
                        "jim",
                        [(0, '{ "type":"register", "name":"jim" }')]
                        + [(0, '{ "type":"move", "action":"FORWARD" }') for i in range(2 * ticks)],
                    ),
                ],
                viewer=None,
                move_timeout=timeout,
                ticks=ticks,
            )
        )

        # Game complete
        self.assertEqual(10, game.game_tick)

    def test_game_server_with_tokens(self):
        team_names_by_token = {"ugralkfad": "teamA", "oijadaas": "teamB"}

        server = SocketGameServer(
            max_nb_ticks=10, max_nb_players=100, team_names_by_token=team_names_by_token, path=path, port=port
        )

        self.assertEqual(team_names_by_token, server.team_names_by_token)

    def test_game_server_with_config(self):
        from pathlib import Path

        root_path = Path(__file__).parent.parent.parent.parent
        file_path = (root_path / "game_presets/0-basic_4p_21x21.txt").resolve()

        gc = GameConfig.from_file(file_path)
        server = SocketGameServer(max_nb_ticks=10, max_nb_players=100, game_config=gc, path=path, port=port)
        self.assertEqual(21, server.game_map.size)
        self.assertEqual(4, server.max_nb_players)

    def test_game_server_with_record_path(self):
        server = SocketGameServer(
            max_nb_ticks=10, max_nb_players=100, path=path, port=port, record_path="./yes-this-is-a/path/file.json"
        )
        self.assertEqual(len(server.game.recorders), 1)

    def test_game_server_with_min_nb_players(self):
        min_nb_players = 5
        server = SocketGameServer(
            max_nb_ticks=10, max_nb_players=100, path=path, port=port, min_nb_players=min_nb_players
        )
        self.assertEqual(server.min_nb_players, min_nb_players)

    def test_game_server_with_team_names_tokens(self):
        team_names_by_token = {}
        team_names_by_token["a"] = "A"
        team_names_by_token["b"] = "B"

        server = SocketGameServer(
            max_nb_ticks=10, max_nb_players=100, path=path, port=port, team_names_by_token=team_names_by_token
        )
        self.assertEqual(server.min_nb_players, 2)

    def test_game_server_with_team_names_tokens_and_min_nb_players(self):
        min_nb_players = 5
        team_names_by_token = {}
        team_names_by_token["a"] = "A"
        team_names_by_token["b"] = "B"

        server = SocketGameServer(
            max_nb_ticks=10,
            max_nb_players=100,
            path=path,
            port=port,
            team_names_by_token=team_names_by_token,
            min_nb_players=min_nb_players,
        )
        self.assertEqual(server.min_nb_players, 2)
