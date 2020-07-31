import unittest

from blitz2020.game.position import Direction
from blitz2020.game.position import Position


class TestPosition(unittest.TestCase):
    def test_init_with_values(self):
        """
        Tests that the position constructor saves to right values
        """

        position = Position(3, 4)
        self.assertEqual(position.x, 3)
        self.assertEqual(position.y, 4)

    def test_move(self):
        """
        Tests that the move method will move the position in the right direction
        """

        self.assertEqual(Position(3, 4).move(Direction(Direction.UP)), Position(3, 3))
        self.assertEqual(Position(3, 4).move((0, -1)), Position(3, 3))

        self.assertEqual(Position(3, 4).move(Direction(Direction.DOWN)), Position(3, 5))
        self.assertEqual(Position(3, 4).move((0, 1)), Position(3, 5))

        self.assertEqual(Position(3, 4).move(Direction(Direction.LEFT)), Position(2, 4))
        self.assertEqual(Position(3, 4).move((-1, 0)), Position(2, 4))

        self.assertEqual(Position(3, 4).move(Direction(Direction.RIGHT)), Position(4, 4))
        self.assertEqual(Position(3, 4).move((1, 0)), Position(4, 4))

    def test_invalid_move(self):
        with self.assertRaises(Exception):
            Position(1, 1).move(other="dummy")

    def test_add(self):
        """
        Tests that the move method will move the position in the right direction
        """

        oldPosition = Position(3, 4)
        newPosition = oldPosition + (0, 1)

        self.assertIsNot(oldPosition, newPosition)
        self.assertEqual(Position(3, 5), newPosition)

    def test_copy_create_new_position(self):
        """
        Tests that copy will create a new position
        """
        oldPosition = Position(3, 5)
        newPosition = oldPosition.copy()

        self.assertIsNot(oldPosition, newPosition)
        self.assertEqual(oldPosition, newPosition)

    def test_eq(self):
        """
        Tests that the __eq__ work
        """

        self.assertEqual(Position(3, 5), Position(3, 5))
        self.assertNotEqual(Position(4, 5), Position(5, 5))

    def test_str(self):
        """
        Tests that __str__ work
        """

        self.assertEqual(Position(3, 5).__str__(), "[x: 3, y: 5]")

        self.assertEqual(Position(3, 5).__str__(), "[x: 3, y: 5]")

    def test_is_next_to_up(self):
        self.assertTrue(Position(0, 0).is_next_to(Position(0, 1)))

    def test_is_next_to_down(self):
        self.assertTrue(Position(0, 1).is_next_to(Position(0, 0)))

    def test_is_next_to_right(self):
        self.assertTrue(Position(1, 0).is_next_to(Position(2, 0)))

    def test_is_next_to_left(self):
        self.assertTrue(Position(1, 0).is_next_to(Position(0, 0)))

    def test_is_next_to_not_next_to_diagonal(self):
        self.assertFalse(Position(1, 1).is_next_to(Position(0, 0)))
        self.assertFalse(Position(2, 2).is_next_to(Position(1, 1)))
        self.assertFalse(Position(2, 0).is_next_to(Position(1, 1)))
        self.assertFalse(Position(0, 2).is_next_to(Position(1, 1)))

    def test_is_next_to_not_next_to(self):
        self.assertFalse(Position(0, 1).is_next_to(Position(5, 5)))

    def test_direction_to_up(self):
        self.assertEqual(Position(1, 1).direction_to(Position(1, 0)), Direction(Direction.UP))

    def test_direction_to_down(self):
        self.assertEqual(Position(1, 1).direction_to(Position(1, 2)), Direction(Direction.DOWN))

    def test_direction_to_left(self):
        self.assertEqual(Position(1, 1).direction_to(Position(0, 1)), Direction(Direction.LEFT))

    def test_direction_to_right(self):
        self.assertEqual(Position(1, 1).direction_to(Position(2, 1)), Direction(Direction.RIGHT))
