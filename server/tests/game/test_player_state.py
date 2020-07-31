import unittest

from blitz2020.game.direction import Direction
from blitz2020.game.game_map import GameMap
from blitz2020.game.player_state import PlayerState
from blitz2020.game.player_state import dir_to_center
from blitz2020.game.position import Position


class TestPlayerState(unittest.TestCase):
    def test_init(self):
        game_map = GameMap(5)
        pos = Position(1, 1)
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=pos)

        self.assertFalse(ps.killed)
        self.assertEqual(ps.score, 0)
        self.assertEqual(ps.spawn_position, pos)
        self.assertEqual(ps.position, pos)
        self.assertEqual(ps.tail, [ps.spawn_position])
        self.assertEqual(ps.direction, Direction.RIGHT)
        self.assertTrue(ps.game_map.is_conquered_by(pos, 1))

    def test_init_with_direction(self):
        game_map = GameMap(5)
        pos = Position(1, 1)
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=pos, direction=Direction(Direction.DOWN))

        self.assertEqual(ps.direction, Direction(Direction.DOWN))

    def test_reset_position(self):
        game_map = GameMap(5)
        pos = Position(1, 1)
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=pos, direction=Direction(Direction.DOWN))
        ps.direction = Direction(Direction.LEFT)
        ps.reset_position()

        self.assertEqual(ps.direction, Direction(Direction.DOWN))

    def test_dir_to_center(self):
        map_size = 5
        self.assertEqual(dir_to_center(Position(0, 0), map_size), Direction.RIGHT)
        self.assertEqual(dir_to_center(Position(0, 1), map_size), Direction.DOWN)
        self.assertEqual(dir_to_center(Position(map_size - 1, 0), map_size), Direction.LEFT)
        self.assertEqual(dir_to_center(Position(map_size - 1, map_size - 2), map_size), Direction.UP)

    def test_add_history(self):
        game_map = GameMap(5)
        pos = Position(1, 1)
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=pos)

        for tick in range(10):
            # add 1 or 2 messages per tick
            for j in range(1 + tick % 2):
                ps.add_history(tick, f"message-{tick}-{j}")

        self.assertEqual(15, len(ps.history))

        # adding one message will pop one oldest
        ps.add_history(11, "message-11")
        self.assertEqual(15, len(ps.history))
        self.assertEqual("message-11", ps.history[0].message)
        self.assertEqual("message-1-1", ps.history[-2].message)
        self.assertEqual("message-1-0", ps.history[-1].message)

        # adding a second message will pop two oldests
        ps.add_history(12, "message-12")
        self.assertEqual(14, len(ps.history))
        self.assertEqual("message-12", ps.history[0].message)
        self.assertEqual("message-2-0", ps.history[-1].message)
