import datetime
import datetime
import json
import unittest

from blitz2020.game.direction import Direction
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState, HistoryItem
from blitz2020.game.player_stats import PlayerStats
from blitz2020.game.position import Position
from blitz2020.servers.socket.utils import (
    game_state_to_json,
    dict_to_player_state,
    dict_to_game_map,
    player_state_to_dict,
    dict_to_game_state,
    game_state_to_dict,
)
from tests.game.map_utils import create_map_with, W, E

state_test = {
    "type": "tick",
    "game": {
        "map": [
            ["W", "W", "W", "W", "W"],
            ["W", "C-0", "C-1", " ", "W"],
            ["W", "W", "C-2", "%-0", "W"],
            ["W", "!", "$", "%", "W"],
            ["W", "W", "W", "W", "W"],
        ],
        "player_id": 1,
        # fmt: off
        "pretty_map":   '[[W     W     W     W     W    ]\n'
                        ' [W     C0    C1P1        W    ]\n'
                        ' [W     WP0   C2P2  %0    W    ]\n'
                        ' [W     !     $     %     W    ]\n'
                        ' [W     W     W     W     W    ]]\n'
                        'DISCLAMER: this map does not have the same content as '
                        'the json game map. Symbols are combined to help you '
                        'visualize every spot on this turn. Hyphen are also '
                        'removed. See the documentation for the json map '
                        'symbol signification.\n'
                        'Symbols added or modified on this map for '
                        'visualization purpose are:\n'
                        'Px: Position of player x - Cx: Conquered by player x '
                        '- Tx: Tail of player x',
        # fmt: on
        "tick": 123,
        "ticks_left": 500,
    },
    "players": [
        {
            "active": True,
            "killed": True,
            "position": {"x": 1, "y": 2},
            "spawn_position": {"x": 1, "y": 1},
            "direction": "RIGHT",
            "spawn_direction": "LEFT",
            "tail": [{"x": 1, "y": 2}],
            "id": 0,
            "name": "p0",
            "score": 123.4,
            "stats": {
                PlayerStats.CONQUERED: 1,
                PlayerStats.KILLS: 1,
                PlayerStats.KILLED: 1,
                PlayerStats.SUICIDES: 1,
                PlayerStats.NEMESIS: "p2",
                "players_killed": {"p1": 1},
                "killed_by_players": {"p2": 1},
            },
            "history": [
                {"timestamp": "1900-01-01T13:14:15.000555", "tick": 11, "message": "message-11"},
                {"timestamp": "1900-01-01T13:14:15.000444", "tick": 10, "message": "message-10"},
            ],
        },
        {
            "active": False,
            "killed": False,
            "position": {"x": 2, "y": 1},
            "spawn_position": {"x": 2, "y": 1},
            "direction": "LEFT",
            "spawn_direction": "RIGHT",
            "tail": [{"x": 2, "y": 1}],
            "id": 1,
            "name": "p1",
            "score": 0,
            "stats": {PlayerStats.CONQUERED: 1, "players_killed": {}, "killed_by_players": {}},
            "history": [],
        },
        {
            "active": True,
            "killed": False,
            "position": {"x": 2, "y": 2},
            "spawn_position": {"x": 2, "y": 2},
            "direction": "LEFT",
            "spawn_direction": "DOWN",
            "tail": [{"x": 2, "y": 1}, {"x": 2, "y": 2}],
            "id": 2,
            "name": "p2",
            "score": 0,
            "stats": {PlayerStats.CONQUERED: 1, "players_killed": {}, "killed_by_players": {}},
            "history": [],
        },
    ],
}


class TestUtils(unittest.TestCase):
    def test_game_state_to_json_player(self):
        gm = create_map_with([[E, E, E], [E, E, E], [E, E, E]])
        gm.set_tile(Position(1, 3), GameMap.BLACK_HOLE)
        gm.set_tile(Position(2, 3), GameMap.BLITZIUM)
        gm.set_tile(Position(3, 3), GameMap.PLANET)
        gm.set_tile(Position(3, 2), GameMap.PLANET, 0)
        p0 = PlayerState(0, "p0", gm, Position(1, 1), direction=Direction(Direction.UP))
        p0.killed = True
        p0.position = Position(3, 1)
        p0.direction = Direction(Direction.RIGHT)
        p0.tail = [p0.spawn_position, Position(2, 1), p0.position]
        p0.score = 123.4
        p0.stats.kill_player("p1")
        p0.stats.killed_by_player("p2")
        p0.stats.add_stat(PlayerStats.SUICIDES)
        p0.history.append(HistoryItem(11, "message-11", datetime.datetime(1900, 1, 1, 13, 14, 15, 555)))
        p0.history.append(HistoryItem(10, "message-10", datetime.datetime(1900, 1, 1, 13, 14, 15, 444)))
        p1 = PlayerState(1, "p1", gm, position=Position(1, 2), direction=Direction(Direction.DOWN))
        p1.active = False
        p1.direction = Direction(Direction.LEFT)
        p2 = PlayerState(2, "p2", gm, Position(2, 2), direction=Direction(Direction.RIGHT))
        p2.direction = Direction(Direction.LEFT)
        gs = GameState(gm, [p0, p1, p2])
        self.maxDiff = 4000
        expected = {
            "type": "tick",
            "game": {
                "map": [
                    ["W", "W", "W", "W", "W"],
                    ["W", "C-0", " ", " ", "W"],
                    ["W", "C-1", "C-2", "%-0", "W"],
                    ["W", "!", "$", "%", "W"],
                    ["W", "W", "W", "W", "W"],
                ],
                "player_id": 1,
                # fmt: off
                "pretty_map":   '[[W     W     W     W     W    ]\n'
                                ' [W     C0T0  T0    P0    W    ]\n'
                                ' [W     C1P1  C2P2  %0    W    ]\n'
                                ' [W     !     $     %     W    ]\n'
                                ' [W     W     W     W     W    ]]\n'
                                'DISCLAMER: this map does not have the same content as '
                                'the json game map. Symbols are combined to help you '
                                'visualize every spot on this turn. Hyphen are also '
                                'removed. See the documentation for the json map '
                                'symbol signification.\n'
                                'Symbols added or modified on this map for '
                                'visualization purpose are:\n'
                                'Px: Position of player x - Cx: Conquered by player x '
                                '- Tx: Tail of player x',
                # fmt: on
                "tick": 123,
                "ticks_left": 500,
            },
            "players": [
                {
                    "active": True,
                    "killed": True,
                    "position": {"x": 3, "y": 1},
                    "spawn_position": {"x": 1, "y": 1},
                    "direction": "RIGHT",
                    "spawn_direction": "UP",
                    "tail": [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}],
                    "id": 0,
                    "name": "p0",
                    "score": 123.4,
                    "stats": {
                        PlayerStats.CONQUERED: 1,
                        PlayerStats.KILLS: 1,
                        PlayerStats.KILLED: 1,
                        PlayerStats.SUICIDES: 1,
                        PlayerStats.NEMESIS: "p2",
                        "players_killed": {"p1": 1},
                        "killed_by_players": {"p2": 1},
                    },
                    "history": [
                        {"timestamp": "1900-01-01T13:14:15.000555", "tick": 11, "message": "message-11"},
                        {"timestamp": "1900-01-01T13:14:15.000444", "tick": 10, "message": "message-10"},
                    ],
                },
                {
                    "active": False,
                    "killed": False,
                    "position": {"x": 1, "y": 2},
                    "spawn_position": {"x": 1, "y": 2},
                    "direction": "LEFT",
                    "spawn_direction": "DOWN",
                    "tail": [{"x": 1, "y": 2}],
                    "id": 1,
                    "name": "p1",
                    "score": 0,
                    "stats": {PlayerStats.CONQUERED: 1, "players_killed": {}, "killed_by_players": {}},
                    "history": [],
                },
                {
                    "active": True,
                    "killed": False,
                    "position": {"x": 2, "y": 2},
                    "spawn_position": {"x": 2, "y": 2},
                    "direction": "LEFT",
                    "spawn_direction": "RIGHT",
                    "tail": [{"x": 2, "y": 2}],
                    "id": 2,
                    "name": "p2",
                    "score": 0,
                    "stats": {PlayerStats.CONQUERED: 1, "players_killed": {}, "killed_by_players": {}},
                    "history": [],
                },
            ],
        }

        # players have an id
        message = game_state_to_json(game_tick=123, player_id=1, game_state=gs, ticks_left=500)
        # print(message)
        data = json.loads(message)

        self.assertEqual(expected, data)

    def test_game_state_to_json_viewer(self):
        gm = create_map_with([[E]])
        gs = GameState(gm)
        self.maxDiff = 999999
        expected = {
            "type": "tick",
            "game": {
                "map": [["W", "W", "W"], ["W", " ", "W"], ["W", "W", "W"]],
                "player_id": None,
                # fmt: off
                "pretty_map":   '[[W     W     W    ]\n'
                                ' [W           W    ]\n'
                                ' [W     W     W    ]]\n'
                                'DISCLAMER: this map does not have the same content as '
                                'the json game map. Symbols are combined to help you '
                                'visualize every spot on this turn. Hyphen are also '
                                'removed. See the documentation for the json map '
                                'symbol signification.\n'
                                'Symbols added or modified on this map for '
                                'visualization purpose are:\n'
                                'Px: Position of player x - Cx: Conquered by player x '
                                '- Tx: Tail of player x',
                # fmt: on
                "tick": 123,
                "ticks_left": 500,
            },
            "players": [],
        }

        # viewers do not have player id
        message = game_state_to_json(game_tick=123, player_id=None, game_state=gs, ticks_left=500)
        data = json.loads(message)

        self.assertEqual(data, expected)

    def test_dict_to_game_map(self):
        data = state_test["game"]["map"]
        new_map = dict_to_game_map(data)

        # fmt: off
        gm = create_map_with([
            [E, E, E],
            [W, E, E],
            [E, E, E]
        ])
        # fmt: on
        gm.set_tile(Position(1, 3), GameMap.BLACK_HOLE)
        gm.set_tile(Position(2, 3), GameMap.BLITZIUM)
        gm.set_tile(Position(3, 3), GameMap.PLANET)
        gm.set_tile(Position(3, 2), GameMap.PLANET, 0)
        gm.conquer_tile(Position(1, 1), 0)
        gm.conquer_tile(Position(2, 1), 1)
        gm.conquer_tile(Position(2, 2), 2)
        self.assertEqual(gm, new_map)

    def test_dict_to_player_state(self):
        data = state_test["players"][0]
        gm = GameMap(20)
        ps = dict_to_player_state(data, gm)
        dict = player_state_to_dict(ps)
        self.assertEqual(data, dict)

    def test_dict_to_game_state(self):
        player_id, gs, ticks_left = dict_to_game_state(state_test)
        data = game_state_to_dict(gs.game_tick, player_id, gs, ticks_left)
        self.assertEqual(data, state_test)

    def create_state(self):
        game_map = GameMap(21)
        game_state = GameState(game_map)
        p0 = game_state.add_player("0")
        p0.stats.kill_player("p1")
        p0.stats.killed_by_player("p2")
        p0.stats.add_stat(PlayerStats.SUICIDES)
        p0.stats.add_stat(PlayerStats.BLITZIUMS)
        p0.stats.add_stat(PlayerStats.CONQUERED)
        p0.tail = [Position(1, 2), Position(2, 3), Position(4, 5)]
        p0.history.append(HistoryItem(11, "message-11", datetime.datetime(1900, 1, 1, 13, 14, 15, 555)))
        p0.history.append(HistoryItem(10, "message-10", datetime.datetime(1900, 1, 1, 13, 14, 15, 444)))

        p1 = game_state.add_player("1")
        p1.stats.kill_player("p1")
        p1.stats.killed_by_player("p2")
        p1.stats.add_stat(PlayerStats.SUICIDES)
        p1.stats.add_stat(PlayerStats.BLITZIUMS)
        p1.stats.add_stat(PlayerStats.CONQUERED)
        p1.tail = [Position(1, 2), Position(2, 3), Position(4, 5)]
        p1.history.append(HistoryItem(11, "message-11", datetime.datetime(1900, 1, 1, 13, 14, 15, 555)))
        p1.history.append(HistoryItem(10, "message-10", datetime.datetime(1900, 1, 1, 13, 14, 15, 444)))

        return game_state

    def test_perf_copy(self):
        import timeit
        import copy

        game_state = self.create_state()

        number = 1000
        elapsed = timeit.timeit(lambda: copy.deepcopy(game_state), number=number)
        # print(elapsed)
