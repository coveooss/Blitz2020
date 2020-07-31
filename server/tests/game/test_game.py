import asyncio
import inspect
import unittest
from unittest.mock import Mock

from asyncmock import AsyncMock
from blitz2020.game.abstract_player import AbstractPlayer
from blitz2020.game.action import Action
from blitz2020.game.game import Game
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.game.position import Position
from blitz2020.players.random_player import RandomPlayer


def get_game(map_size=10, max_nb_ticks=20, move_timeout: float = 2):
    game_map = GameMap(map_size)
    game_state = GameState(game_map)
    game = Game(game_state=game_state, max_nb_ticks=max_nb_ticks, move_timeout=move_timeout)
    return game


class DummyPlayer(AbstractPlayer):
    def __init__(self, body):
        super().__init__("dummy")
        self.body = body

    async def request_next_move(self, game_tick: int, game_state: GameState) -> Action:
        if inspect.iscoroutinefunction(self.body):
            return await self.body(game_tick, game_state)
        else:
            return self.body(game_tick, game_state)

    async def request_next_move_impl(self, game_tick: int, game_state: GameState) -> Action:
        pass


class TestGame(unittest.TestCase):
    def test_register_player(self):
        game = get_game()
        player1 = Mock()
        game.register_player(player1)
        player1.set_player_state.assert_called_once()
        player1.close.assert_not_called()
        player1.request_next_move.assert_not_called()

    def test_register_random_player(self):
        game = get_game()
        player1 = RandomPlayer()
        game.register_player(player1)
        self.assertTrue(player1.player_state is not None)

    def test_small_single_player_game(self):
        game = get_game(max_nb_ticks=10)
        game.register_player(RandomPlayer())
        viewer = AsyncMock()
        game.register_viewer(viewer)
        asyncio.run(game.game_loop())
        self.assertEqual(10, viewer.send_tick.call_count)
        self.assertEqual(1, viewer.send_winner.call_count)

    def test_small_multi_player_game(self):
        game = get_game(max_nb_ticks=20)
        [game.register_player(RandomPlayer()) for _ in range(4)]
        asyncio.run(game.game_loop())

    def test_unregister_last_player_stop_game(self):
        game = get_game()
        game.is_started = True  # simulate started game
        player = RandomPlayer()
        game.register_player(player)
        game.unregister_player(player)
        self.assertFalse(game.is_started)

    def test_register_viewer(self):
        game = get_game()
        viewer = Mock()
        game.register_viewer(viewer)
        self.assertEqual(len(game.viewers), 1)
        game.unregister_viewer(viewer)
        self.assertEqual(len(game.viewers), 0)

    def test_move_forward_if_timeout(self):
        move_timeout = 0.001
        game = get_game(move_timeout=move_timeout)
        game.game_tick = 10

        async def slow(game_tick, game_state):
            await asyncio.sleep(2 * move_timeout)
            return (game_tick, Action.TURN_LEFT)

        player = DummyPlayer(slow)
        game.register_player(player)
        next_move = asyncio.run(game.request_next_move(player))
        self.assertEqual(next_move, Action.FORWARD)

    def test_move_forward_if_error(self):
        game = get_game()

        def raiseException(game_tick, game_state):
            raise Exception

        player = DummyPlayer(raiseException)
        game.register_player(player)
        next_move = asyncio.run(game.request_next_move(player))
        self.assertEqual(next_move, Action.FORWARD)

    def test_move_forward_if_invalid_tick(self):
        game = get_game()

        def invalid_tick(game_tick, game_state):
            return (game_tick + 10, Action.TURN_LEFT)

        player = DummyPlayer(invalid_tick)
        game.register_player(player)
        next_move = asyncio.run(game.request_next_move(player))
        self.assertEqual(next_move, Action.FORWARD)

    def test_skip_player_if_inactive(self):
        game = get_game()
        player = DummyPlayer(lambda x, y: (x, Action.TURN_LEFT))
        game.register_player(player)
        player.player_state.active = False
        next_move = asyncio.run(game.request_next_move(player))
        self.assertEqual(next_move, None)

    def test_skip_player_turn_if_killed(self):
        game = get_game()
        player = DummyPlayer(lambda x, y: (x, Action.TURN_LEFT))
        game.register_player(player)
        player.player_state.killed = True
        player.player_state.position = Position(0, 0)
        next_move = asyncio.run(game.request_next_move(player))
        self.assertEqual(next_move, None)
        self.assertEqual(player.player_state.position, player.player_state.spawn_position)

    def test_register_recorder(self):
        game = get_game()
        recorder = Mock()
        game.register_recorder(recorder)
        self.assertEqual(len(game.recorders), 1)
        game.unregister_recorder(recorder)
        self.assertEqual(len(game.recorders), 0)


def print_scores(game: Game):
    print("----------------")
    for p in game.players:
        print(p.player_state)
    print(f"WINNER: {game.players[0].name_str()}")
