import unittest
from game_message import *


class TestGameMessage(unittest.TestCase):
    def setUp(self):
        with open("game_message.json", "r") as file:
            self.game_message: GameMessage = GameMessage.from_json(file.read())

    @staticmethod
    def get_tile_type(raw_tile: str) -> "TileType":
        if raw_tile == TileType.EMPTY.value:
            return TileType.EMPTY
        elif raw_tile == TileType.ASTEROIDS.value:
            return TileType.ASTEROIDS
        elif raw_tile == TileType.PLANET.value:
            return TileType.PLANET
        elif raw_tile == TileType.BLITZIUM.value:
            return TileType.BLITZIUM
        elif raw_tile == TileType.BLACK_HOLE.value:
            return TileType.BLACK_HOLE
        elif raw_tile.startswith(TileType.CONQUERED.value):
            return TileType.CONQUERED
        elif raw_tile.startswith(TileType.CONQUERED_PLANET.value):
            return TileType.CONQUERED_PLANET
        else:
            return None

    def test_get_tile_type(self):
        posy = 0
        for y in self.game_message.game.map:
            posx = 0
            for x in y:
                self.assertEqual(TileType.get_tile_type(x), TestGameMessage.get_tile_type(x))
                self.assertEqual(
                    self.game_message.game.get_tile_type_at(Point(x=posx, y=posy)), TestGameMessage.get_tile_type(x)
                )
                posx += 1

            posy += 1

    def test_get_tile_owner_id(self):
        posy = 0
        for y in self.game_message.game.map:
            posx = 0
            for x in y:
                try:
                    owner_id = self.game_message.game.get_tile_owner_id(Point(x=posx, y=posy))
                except Exception:
                    self.assertFalse("-" in y)
                posx += 1

            posy += 1
