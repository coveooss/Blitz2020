import unittest

from blitz2020.game.flood import flood


class TestFlood(unittest.TestCase):
    def test_all(self):
        size = 10
        tiles = [[1] * size for _ in range(size)]
        flood(tiles, 1, 0)
        self.assertEqual(tiles, [[0] * size for _ in range(size)])

    def test_none(self):
        size = 10
        tiles = [[0] * size for _ in range(size)]
        flood(tiles, 1, 0)
        self.assertEqual(tiles, [[0] * size for _ in range(size)])

    def test_closed_box(self):
        tiles = [
            # fmt: off
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
            # fmt: on
        ]
        flood(tiles, 1, 0)

        expected = [
            # fmt: off
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
            # fmt: on
        ]
        self.assertEqual(tiles, expected)

    def test_closed_box_corner(self):
        # This test case is not possible by construction wince we have an asteroids around the map
        tiles = [
            # fmt: off
            [1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1]
            # fmt: on
        ]
        flood(tiles, 1, 0)

        expected = [
            # fmt: off
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
            # fmt: on
        ]
        self.assertEqual(tiles, expected)

    def test_open_path(self):
        tiles = [
            # fmt: off
            [1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
            # fmt: on
        ]
        size = len(tiles)
        flood(tiles, 1, 0)
        self.assertEqual(tiles, [[0] * size for _ in range(size)])

    def simple_flood(self):
        map_size = 21
        flooded_tiles = [[1] * map_size for _ in range(map_size)]
        flooded_tiles[5][5] = 0
        flooded_tiles[5][6] = 0
        flooded_tiles[6][5] = 0
        flooded_tiles[6][6] = 0
        flood(flooded_tiles, 1, 0)

    def test_perf_flood(self):
        import timeit

        number = 1000
        elapsed = timeit.timeit(lambda: self.simple_flood(), number=number)
        # print(elapsed)
