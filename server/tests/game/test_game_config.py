import unittest
from pathlib import Path

from blitz2020.game.direction import Direction
from blitz2020.game.game_config import GameConfig
from blitz2020.game.game_map import GameMap
from blitz2020.game.position import Position

root_path = Path(__file__).parent.parent.parent


class TestGameconfig(unittest.TestCase):
    def test_from_str(self):
        data = """
            WWWWW
            W!%$W
            W1 3W
            W4W2W
            WWWWW\r\n
        """
        gc = GameConfig.from_str(data)

        self.assertEqual(gc.game_map.size, 5)
        self.assertEqual(gc.game_map.get_tile(Position(1, 1)), (GameMap.BLACK_HOLE, None))
        self.assertEqual(gc.game_map.get_tile(Position(2, 1)), (GameMap.PLANET, None))
        self.assertEqual(gc.game_map.get_tile(Position(3, 1)), (GameMap.BLITZIUM, None))
        self.assertEqual(gc.game_map.get_tile(Position(2, 2)), (GameMap.EMPTY, None))
        self.assertEqual(gc.game_map.get_tile(Position(2, 3)), (GameMap.ASTEROIDS, None))
        self.assertEqual(gc.spawn_positions, [Position(1, 2), Position(3, 3), Position(3, 2), Position(1, 3)])

    def test_from_str_non_square(self):
        data = """
            WWW
            W  W
            WWW
        """
        with self.assertRaises(Exception):
            GameConfig.from_str(data)

    def test_from_str_invalid_tile(self):
        data = """
            WWW
            WxW
            WWW
        """
        with self.assertRaises(Exception):
            GameConfig.from_str(data)

    def test_from_file(self):
        file_path = (root_path / "game_presets/0-basic_4p_21x21.txt").resolve()
        gc = GameConfig.from_file(file_path)
        self.assertEqual(21, gc.game_map.size)
        self.assertEqual(4, len(gc.spawn_positions))

    def test_with_direction(self):
        data = """
               WWWWWW
               W1  3W
               WD  DW
               WD  DW
               W4  2W
               WWWWWW\r\n
           """
        gc = GameConfig.from_str(data)

        self.assertEqual(gc.spawn_positions, [Position(1, 1), Position(4, 4), Position(4, 1), Position(1, 4)])
        self.assertEqual(
            gc.spawn_directions,
            [Direction(Direction.DOWN), Direction(Direction.UP), Direction(Direction.DOWN), Direction(Direction.UP)],
        )
