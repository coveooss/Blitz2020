import asyncio
import json
import unittest

import websockets
from asyncmock import AsyncMock, Mock
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState
from blitz2020.game.position import Position
from blitz2020.servers.socket.socket_viewer import SocketViewer


class TestSocketViewer(unittest.TestCase):
    def test_send_tick(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        socket = AsyncMock()
        viewer = SocketViewer(server, socket)

        gs = GameState(GameMap(3))
        nb = 10
        for i in range(nb):
            asyncio.run(viewer.send_tick(100 + i, gs))

        self.assertEqual(nb, socket.send.call_count)
        data = json.loads(socket.send.call_args[0][0])

        self.assertEqual(data["type"], "tick")
        self.assertEqual(data["game"]["tick"], 100 + nb - 1)

    def test_send_tick_socket_closed(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        socket = AsyncMock()
        socket.send.side_effect = websockets.ConnectionClosed(0, "")
        viewer = SocketViewer(server, socket)
        viewer.logger = Mock()

        gs = GameState(GameMap(3))
        asyncio.run(viewer.send_tick(123, gs))

        viewer.logger.warning.assert_called_once()
        server.game.unregister_viewer.assert_called_once()

    def test_send_tick_exception(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        socket = AsyncMock()
        socket.send.side_effect = Exception()
        viewer = SocketViewer(server, socket)
        viewer.logger = Mock()

        gs = GameState(GameMap(3))
        asyncio.run(viewer.send_tick(123, gs))

        viewer.logger.warning.assert_called_once()
        server.game.unregister_viewer.assert_called_once()
        socket.close.assert_called_once()

    def test_send_winner(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        socket = AsyncMock()
        viewer = SocketViewer(server, socket)

        gs = GameState(GameMap(3))
        ps = PlayerState(1, "p1", gs.game_map, Position(1, 1))
        asyncio.run(viewer.send_winner(123, ps))

        socket.send.assert_called_once()
        data = json.loads(socket.send.call_args[0][0])

        self.assertEqual(data["type"], "winner")
        self.assertEqual(data["tick"], 123)
        self.assertEqual(data["winner"]["name"], "p1")

    def test_send_winner_socket_closed(self):
        server = Mock()
        socket = AsyncMock()
        socket.send.side_effect = websockets.ConnectionClosed(0, "")
        viewer = SocketViewer(server, socket)
        viewer.logger = Mock()

        gs = GameState(GameMap(3))
        ps = PlayerState(1, "p1", gs.game_map, Position(1, 1))
        asyncio.run(viewer.send_winner(123, ps))

        viewer.logger.warning.assert_called_once()
        server.game.unregister_viewer.assert_called_once()

    def test_send_winner_exception(self):
        server = Mock()
        socket = AsyncMock()
        socket.send.side_effect = Exception()
        viewer = SocketViewer(server, socket)
        viewer.logger = Mock()

        gs = GameState(GameMap(3))
        ps = PlayerState(1, "p1", gs.game_map, Position(1, 1))
        asyncio.run(viewer.send_winner(123, ps))

        viewer.logger.warning.assert_called_once()
        server.game.unregister_viewer.assert_called_once()
        socket.close.assert_called_once()
