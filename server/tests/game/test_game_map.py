import unittest

from blitz2020.game.game_map import GameMap, InvalidStateException
from blitz2020.game.game_map import OutOfBoundExeption
from blitz2020.game.position import Position
from tests.game.map_utils import create_map_with, W, E


class TestMap(unittest.TestCase):
    def setUp(self):
        self.map_size = 10
        self.my_map = GameMap(self.map_size)

    def test_init_with_empty_map(self):
        """
        Test that a new map will be empty and the correct size
        """
        self.assertEqual(self.my_map.size, self.map_size)
        self.assertEqual(len(self.my_map.tiles), self.my_map.size)
        [self.assertEqual(len(self.my_map.tiles[y]), self.my_map.size) for y in range(self.my_map.size)]

        # there is an asteroids around the map
        self.assertEqual(self.my_map.empty_tiles, (self.map_size - 2) ** 2)

        for y in range(self.map_size):
            for x in range(self.map_size):
                pos = Position(x=x, y=y)
                self.assertFalse(self.my_map.is_out_of_bound(pos))

                if x == 0 or x == self.map_size - 1 or y == 0 or y == self.map_size - 1:
                    # check asteroids
                    self.assertFalse(self.my_map.is_empty(pos))
                    self.assertEqual(self.my_map.tiles[y][x], (GameMap.ASTEROIDS, None))
                    self.assertTrue(self.my_map.is_asteroids(pos))
                    self.assertEqual(self.my_map.get_tile(Position(x=x, y=y)), (GameMap.ASTEROIDS, None))
                else:
                    # must be empty
                    self.assertTrue(self.my_map.is_empty(pos))
                    self.assertFalse(self.my_map.is_asteroids(pos))
                    self.assertEqual(self.my_map.get_tile(Position(x=x, y=y)), (GameMap.EMPTY, None))

    def test_eq(self):
        self.assertEqual(GameMap(5), GameMap(5))
        self.assertNotEqual(GameMap(5), GameMap(6))

        map_data1 = [[E, W, W], [E, 1, 2], [E, 3, E]]
        map_data2 = [[E, W, W], [E, 2, 3], [E, 1, E]]
        self.assertEqual(create_map_with(map_data1), create_map_with(map_data1))
        self.assertNotEqual(create_map_with(map_data1), create_map_with(map_data2))

    def test_str(self):
        map = create_map_with(
            [
                # fmt: off
                [W, E, E],
                [E, 0, E],
                [E, E, 1]
                # fmt: on
            ]
        )
        map.set_tile(Position(2, 1), state=GameMap.PLANET, player_id=0)
        map.set_tile(Position(3, 1), state=GameMap.BLACK_HOLE)
        self.assertTrue(map.is_black_hole(Position(3, 1)))
        map.set_tile(Position(3, 2), state=GameMap.BLITZIUM)
        self.assertTrue(map.is_blitzium(Position(3, 2)))
        str_map = str(map)
        expected = "\n".join(
            [
                # fmt: off
                'WWWWW',
                'WW%!W',
                'W 0$W',
                'W  1W',
                'WWWWW'
                # fmt: on
            ]
        )
        self.assertEqual(str_map, expected)

    def test_cannot_overwrite_asteroids(self):
        # Ok to write an asteroids on an asteroids
        self.my_map.set_tile(Position(x=0, y=0), state=GameMap.ASTEROIDS)

        # Invalid to overwrite an asteroids with something else
        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(Position(x=0, y=0), state=GameMap.EMPTY, player_id=0)

        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(Position(x=0, y=0), state=GameMap.EMPTY)

    def test_cannot_overwrite_planet(self):
        # Ok to write a planet on a planet (take ownership)
        pos = Position(x=1, y=1)
        self.my_map.set_tile(pos, state=GameMap.PLANET, player_id=None)
        self.my_map.set_tile(pos, state=GameMap.PLANET, player_id=1)
        self.my_map.set_tile(pos, state=GameMap.PLANET, player_id=2)
        self.my_map.set_tile(pos, state=GameMap.PLANET, player_id=None)
        self.my_map.set_tile(pos, state=GameMap.PLANET, player_id=3)

        # Invalid to overwrite a planet with something else
        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.BLACK_HOLE)

        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.ASTEROIDS)

        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.BLITZIUM)

        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.EMPTY)

    def test_invalid_set_title(self):
        pos = Position(x=1, y=1)

        # cannot have player id
        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.ASTEROIDS, player_id=1)
        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.BLITZIUM, player_id=1)
        with self.assertRaises(InvalidStateException):
            self.my_map.set_tile(pos, state=GameMap.BLACK_HOLE, player_id=1)

    def test_get_set_tile(self):
        """
        Test that you can set a tile and get it back
        """
        position = Position(x=2, y=1)
        old_is_empty = self.my_map.empty_tiles
        self.assertTrue(self.my_map.is_empty(position))
        self.assertEqual(self.my_map.get_tile(position), GameMap.empty_tile)

        # conquer empty tile is the same as setting an owner on it
        self.my_map.set_tile(position, GameMap.EMPTY, 1)
        self.assertFalse(self.my_map.is_empty(position))
        self.assertTrue(self.my_map.is_conquered_by(position, 1))
        self.assertEqual(self.my_map.get_owner(position), 1)
        self.assertEqual(self.my_map.get_tile(position), (GameMap.EMPTY, 1))
        self.assertEqual(self.my_map.empty_tiles, old_is_empty - 1)

        # clear tile remove owner
        self.my_map.clear_tile(position)
        self.assertTrue(self.my_map.is_empty(position))
        self.assertEqual(self.my_map.get_tile(position)[0], GameMap.EMPTY)
        self.assertEqual(self.my_map.empty_tiles, old_is_empty)

        with self.assertRaises(OutOfBoundExeption):
            self.my_map.get_tile(Position(self.map_size + 10, self.map_size + 10))

        with self.assertRaises(OutOfBoundExeption):
            self.my_map.set_tile(Position(self.map_size + 10, self.map_size + 10), GameMap.EMPTY, 1)

    def test_get_owner(self):
        """
        Test that you can get the tile owner
        """
        position = Position(1, 1)
        self.assertTrue(self.my_map.is_empty(position))
        self.assertEqual(self.my_map.get_owner(position), None)

        self.my_map.conquer_tile(position, player_id=1)
        self.assertEqual(self.my_map.get_owner(position), 1)

        self.my_map.conquer_tile(position, player_id=0)
        self.assertEqual(self.my_map.get_owner(position), 0)

        self.my_map.set_tile(position, GameMap.PLANET, player_id=None)
        self.assertEqual(self.my_map.get_owner(position), None)

        self.my_map.conquer_tile(position, player_id=0)
        self.assertEqual(self.my_map.get_owner(position), 0)

        with self.assertRaises(OutOfBoundExeption):
            self.my_map.get_owner(Position(self.map_size + 10, self.map_size + 10))

    def test_is_conquered_by(self):
        """
        Test that you can identify tiles owned by you
        """

        position = Position(1, 1)
        self.assertTrue(self.my_map.is_empty(position))
        self.assertFalse(self.my_map.is_conquered_by(position, player_id=1))

        self.my_map.conquer_tile(position, player_id=1)
        self.assertTrue(self.my_map.is_conquered_by(position, player_id=1))
        self.assertFalse(self.my_map.is_conquered_by(position, player_id=0))

        self.my_map.set_tile(position, GameMap.PLANET, player_id=None)
        self.my_map.conquer_tile(position, player_id=1)
        self.assertTrue(self.my_map.is_conquered_by(position, player_id=1))
        self.assertEqual(self.my_map.get_tile(position), (GameMap.PLANET, 1))

        with self.assertRaises(OutOfBoundExeption):
            self.my_map.is_conquered_by(Position(self.map_size + 10, self.map_size + 10), player_id=0)

    def test_is_out_of_bound(self):
        """
        Test that a position is out of bound for the current map
        """

        self.assertTrue(self.my_map.is_out_of_bound(Position(-self.map_size, 5)))
        self.assertTrue(self.my_map.is_out_of_bound(Position(self.map_size, 5)))
        self.assertTrue(self.my_map.is_out_of_bound(Position(5, -self.map_size)))
        self.assertTrue(self.my_map.is_out_of_bound(Position(5, self.map_size)))
        self.assertTrue(self.my_map.is_out_of_bound(Position(self.map_size, self.map_size)))
        self.assertTrue(self.my_map.is_out_of_bound(Position(-self.map_size, -self.map_size)))

        self.assertFalse(self.my_map.is_out_of_bound(Position(0, 0)))
        self.assertFalse(self.my_map.is_out_of_bound(Position(5, 5)))
        self.assertFalse(self.my_map.is_out_of_bound(Position(self.map_size - 1, self.map_size - 1)))

    def test_clear_tile_owned_by(self):
        """
        Tests that test_clear_tile_owned_by only clear tiles owned by the right player
        """
        self.my_map.set_tile(Position(5, 5), GameMap.PLANET, player_id=None)
        self.my_map.conquer_tile(Position(5, 5), player_id=1)
        self.my_map.conquer_tile(Position(5, 6), player_id=1)
        self.my_map.conquer_tile(Position(5, 7), player_id=1)
        self.my_map.conquer_tile(Position(1, 5), player_id=2)
        self.assertEqual(self.my_map.count_tiles_owned_by(player_id=1), 3)

        self.my_map.clear_tile_owned_by(player_id=1)
        self.assertEqual(self.my_map.count_tiles_owned_by(player_id=1), 0)

        self.assertFalse(self.my_map.is_empty(Position(5, 5)))
        self.assertEqual(self.my_map.get_tile(Position(5, 5)), (GameMap.PLANET, None))
        self.assertTrue(self.my_map.is_empty(Position(7, 5)))

        self.assertEqual(self.my_map.get_tile(Position(1, 5)), (GameMap.EMPTY, 2))
        self.assertEqual(self.my_map.get_owner(Position(1, 5)), 2)

    def test_find_path_empty_tiles(self):
        map = create_map_with(
            [
                # fmt: off
                [1, E, E, E],
                [W, W, E, E],
                [W, E, E, W],
                [2, E, W, E]
                # fmt: on
            ]
        )
        found, path = map.find_path(start=Position(1, 1), goal=Position(4, 1))
        self.assertTrue(found)
        self.assertEqual(len(path), 4)
        self.assertEqual(path, [Position(1, 1), Position(2, 1), Position(3, 1), Position(4, 1)])

        found, path = map.find_path(start=Position(1, 1), goal=Position(1, 4))
        self.assertTrue(found)
        self.assertEqual(len(path), 8)

        found, path = map.find_path(start=Position(1, 1), goal=Position(4, 4))
        self.assertFalse(found)

    def test_find_path_conquered_tiles(self):
        map = create_map_with(
            [
                # fmt: off
                [1, 1, E, 1],
                [E, 1, E, 2],
                [E, 1, E, 1],
                [E, 1, 1, E]
                # fmt: on
            ]
        )
        found, path = map.find_path(start=Position(1, 1), goal=Position(3, 4), player_id=1)
        self.assertTrue(found)
        self.assertEqual(len(path), 6)
        self.assertEqual(
            path, [Position(1, 1), Position(2, 1), Position(2, 2), Position(2, 3), Position(2, 4), Position(3, 4)]
        )

        found, path = map.find_path(start=Position(1, 1), goal=Position(4, 1), player_id=1)
        self.assertFalse(found)

        found, path = map.find_path(start=Position(4, 1), goal=Position(4, 3), player_id=1)
        self.assertFalse(found)

        with self.assertRaises(Exception):
            map.find_path(start=Position(4, 1), goal=Position(4, 2), player_id=1)

        with self.assertRaises(Exception):
            map.find_path(start=Position(3, 1), goal=Position(4, 1), player_id=1)

    def test_get_random_empty_position(self):
        positions = set()

        map_size = 10
        game_map = GameMap(map_size)

        for i in range(25):
            pos = game_map.get_random_empty_position()
            self.assertNotIn(pos, positions)
            self.assertTrue(game_map.is_empty(pos))
            game_map.conquer_tile(pos, i)
            positions.add(pos)

    def test_get_empty_tiles(self):
        map = GameMap(4)
        self.assertEqual(map.get_empty_tiles(), [Position(1, 1), Position(1, 2), Position(2, 1), Position(2, 2)])

        map.set_tile(Position(1, 1), GameMap.PLANET)
        self.assertEqual(map.get_empty_tiles(), [Position(1, 2), Position(2, 1), Position(2, 2)])

        map.set_tile(Position(1, 1), GameMap.PLANET, 1)
        self.assertEqual(map.get_empty_tiles(), [Position(1, 2), Position(2, 1), Position(2, 2)])

        map.set_tile(Position(1, 2), GameMap.ASTEROIDS)
        self.assertEqual(map.get_empty_tiles(), [Position(2, 1), Position(2, 2)])

        map.set_tile(Position(2, 1), GameMap.BLITZIUM)
        self.assertEqual(map.get_empty_tiles(), [Position(2, 2)])

        map.set_tile(Position(2, 1), GameMap.BLACK_HOLE)
        self.assertEqual(map.get_empty_tiles(), [Position(2, 2)])

        map.set_tile(Position(2, 1), GameMap.EMPTY, 1)
        self.assertEqual(map.get_empty_tiles(), [Position(2, 2)])
