import unittest

from asyncmock import Mock
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.recorders.json_recorder import JsonRecorder


class TestJsonRecorder(unittest.TestCase):
    def test_record_tick(self):
        server = Mock()
        server.game.max_nb_ticks = 500
        recorder = JsonRecorder(server.game, "/tmp/out.json")

        gs = GameState(GameMap(3))
        nb = 10
        for i in range(nb):
            recorder.record_tick(100 + i, gs)

        self.assertEqual(len(recorder.ticks), nb)
