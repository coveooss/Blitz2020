import unittest

from blitz2020.game.action import Action
from blitz2020.game.position import Direction


class TestDirection(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Direction("UP"), Direction((0, -1)))
        self.assertEqual(Direction("DOWN"), Direction((0, 1)))
        self.assertEqual(Direction("LEFT"), Direction((-1, 0)))
        self.assertEqual(Direction("RIGHT"), Direction((1, 0)))
        self.assertEqual(Direction(Direction(Direction.UP)), Direction((0, -1)))
        self.assertEqual(Direction("RIGHT"), Direction.RIGHT)

    def test_str(self):
        self.assertEqual(Direction(Direction.UP).to_string(), Direction.UP)
        self.assertEqual(Direction(Direction.UP).__str__(), "[UP, (dx: 0, dy: -1)]")

    def test_change_direction(self):
        dirs = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]

        for i in range(len(dirs)):
            # Going forward do not change direction
            self.assertEqual(Direction(dirs[i]).change_direction(Action.FORWARD), Direction(dirs[i]))

            # turn left
            self.assertEqual(
                Direction(dirs[i]).change_direction(Action.TURN_LEFT), Direction(dirs[(i + 1) % len(dirs)])
            )

            # turn right
            self.assertEqual(
                Direction(dirs[i]).change_direction(Action.TURN_RIGHT), Direction(dirs[(i - 1) % len(dirs)])
            )

    def test_delta(self):
        self.assertEqual(Direction(Direction.UP).delta(), (0, -1))
        self.assertEqual(Direction(Direction.UP).dx(), 0)
        self.assertEqual(Direction(Direction.UP).dy(), -1)

    def test_invalid(self):
        with self.assertRaises(Exception):
            Direction("invalid")

        with self.assertRaises(Exception):
            Direction(("a", "b"))

        with self.assertRaises(Exception):
            Direction((-10, 0))

    def test_copy_create_new_direction(self):
        """
        Tests that copy will create a new direction
        """
        oldDir = Direction(Direction.UP)
        newDir = oldDir.copy()

        self.assertIsNot(oldDir, newDir)
        self.assertEqual(oldDir, newDir)
