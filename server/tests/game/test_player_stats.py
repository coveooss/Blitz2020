import unittest

from blitz2020.game.player_stats import PlayerStats


class TestPlayerStats(unittest.TestCase):
    def test_add_stat(self):
        stats = PlayerStats()

        # countable stats
        stats.add_stat(PlayerStats.KILLS)
        self.assertEqual(1, stats.stats[PlayerStats.KILLS])

        stats.add_stat(PlayerStats.KILLS)
        self.assertEqual(2, stats.stats[PlayerStats.KILLS])

        stats.add_stat(PlayerStats.KILLED)
        stats.add_stat(PlayerStats.PLANETS)
        stats.add_stat(PlayerStats.BLITZIUMS)
        stats.add_stat(PlayerStats.SUICIDES)
        stats.add_stat(PlayerStats.CONQUERED)

        # not countable:
        with self.assertRaises(Exception):
            stats.add_stat(PlayerStats.NEMESIS)

    def test_set_stat(self):
        stats = PlayerStats()

        stats.set_stat(PlayerStats.NEMESIS, "abc")
        self.assertEqual("abc", stats.stats[PlayerStats.NEMESIS])

        # OK to set number for counted stats
        stats.set_stat(PlayerStats.CONQUERED, 123)
        self.assertEqual(123, stats.stats[PlayerStats.CONQUERED])

        # countable stats need a number
        with self.assertRaises(Exception):
            stats.set_stat(PlayerStats.KILLS, "abc")

    def test_kill_player(self):
        stats = PlayerStats()

        player = "abc"

        stats.kill_player(player)
        self.assertEqual(1, stats.stats[PlayerStats.KILLS])
        self.assertEqual(1, stats.kills[player])
        self.assertEqual(1, len(stats.stats))
        self.assertEqual(0, len(stats.killed_by_players))

        stats.kill_player(player)
        self.assertEqual(2, stats.stats[PlayerStats.KILLS])
        self.assertEqual(2, stats.kills[player])

        player2 = "xyz"
        stats.kill_player(player2)
        self.assertEqual(3, stats.stats[PlayerStats.KILLS])
        self.assertEqual(1, stats.kills[player2])

        with self.assertRaises(Exception):
            stats.kill_player("")

    def test_killed_by_player(self):
        stats = PlayerStats()

        player = "b"

        stats.killed_by_player(player)
        self.assertEqual(1, stats.stats[PlayerStats.KILLED])
        self.assertEqual(1, stats.killed_by_players[player])
        self.assertEqual(player, stats.stats[PlayerStats.NEMESIS])
        self.assertEqual(2, len(stats.stats))
        self.assertEqual(0, len(stats.kills))

        player2 = "a"

        stats.killed_by_player(player2)
        stats.killed_by_player(player2)
        self.assertEqual(3, stats.stats[PlayerStats.KILLED])
        self.assertEqual(1, stats.killed_by_players[player])
        self.assertEqual(2, stats.killed_by_players[player2])
        self.assertEqual(player2, stats.stats[PlayerStats.NEMESIS])
        self.assertEqual(0, len(stats.kills))

        with self.assertRaises(Exception):
            stats.killed_by_player("")
