import asyncio
import unittest

import websockets
from asyncmock import AsyncMock, Mock
from blitz2020.game.action import Action
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState
from blitz2020.game.position import Position
from blitz2020.servers.socket.socket_player import SocketPlayer


class TestSocketPlayer(unittest.TestCase):
    def test_valid(self):
        next_move, player = request_next_move('{ "type":"move", "action":"TURN_LEFT", "tick": 123 }')
        self.assertEqual((123, Action.TURN_LEFT), next_move)
        player.logger.warning.assert_not_called()
        player.server.unregister_player.assert_not_called()

    def test_invalid_action(self):
        next_move, player = request_next_move('{ "type":"move", "action":"TURN_XYZ", "tick": 123 }')
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.unregister_player.assert_not_called()
        self.assertTrue(len(player.player_state.history) > 0)

    def test_invalid_type(self):
        next_move, player = request_next_move('{ "type":"xyz", "action":"TURN_RIGHT", "tick": 123 }')
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.unregister_player.assert_not_called()
        self.assertTrue(len(player.player_state.history) > 0)

    def test_invalid_json(self):
        next_move, player = request_next_move("{ abcd }")
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.unregister_player.assert_not_called()
        self.assertTrue(len(player.player_state.history) > 0)

    def test_missing_type_field(self):
        next_move, player = request_next_move('{ "aaa":"xyz", "action":"TURN_RIGHT", "tick": 123 }')
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.unregister_player.assert_not_called()
        self.assertTrue(len(player.player_state.history) > 0)

    def test_missing_action_field(self):
        next_move, player = request_next_move('{ "type":"move" }')
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.unregister_player.assert_not_called()
        self.assertTrue(len(player.player_state.history) > 0)

    def test_socket_closed(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        socket = AsyncMock()
        socket.recv.side_effect = websockets.ConnectionClosed(0, "")
        gs, player = get_player(server, socket)
        player.logger = Mock()
        next_move = asyncio.run(player.request_next_move(123, gs))
        socket.send.assert_called_once()
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.game.unregister_player.assert_called_once()

    def test_exception(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        socket = AsyncMock()
        socket.recv.side_effect = Exception("dummy")
        gs, player = get_player(server, socket)
        player.logger = Mock()
        next_move = asyncio.run(player.request_next_move(123, gs))
        socket.send.assert_called_once()
        self.assertEqual((None, Action.FORWARD), next_move)
        player.logger.warning.assert_called_once()
        player.server.game.unregister_player.assert_not_called()
        self.assertTrue(len(player.player_state.history) > 0)


def get_player(server, socket):
    gs = GameState(GameMap(3))
    player = SocketPlayer(server, "p1", socket)
    player.set_player_state(PlayerState(1, "p1", gs.game_map, Position(1, 1)))
    return gs, player


def request_next_move(return_value):
    server = Mock()
    server.game.max_nb_ticks = 500
    socket = AsyncMock()
    socket.recv.return_value = return_value
    gs, player = get_player(server, socket)
    player.logger = Mock()
    next_move = asyncio.run(player.request_next_move(123, gs))
    socket.send.assert_called_once()
    return next_move, player
