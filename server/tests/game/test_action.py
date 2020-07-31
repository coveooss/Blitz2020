import unittest

from blitz2020.game.action import Action


class TestAction(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Action["FORWARD"], Action.FORWARD)
        self.assertEqual(Action["TURN_LEFT"], Action.TURN_LEFT)
        self.assertEqual(Action["TURN_RIGHT"], Action.TURN_RIGHT)

    def test_invalid(self):
        self.assertRaises(KeyError, lambda: Action["dummy"])
