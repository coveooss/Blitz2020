import unittest

from blitz2020.game.action import Action
from blitz2020.game.direction import Direction
from blitz2020.game.game_config import GameConfig
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState
from blitz2020.game.player_stats import PlayerStats

from tests.game.map_utils import *


class TestGameState(unittest.TestCase):
    def test_add_player(self):
        gs = GameState(GameMap(20), players=None)
        self.assertEqual(len(gs.players), 0)

        nb_players = 10
        for i in range(nb_players):
            gs.add_player(str(i))
        self.assertEqual(len(gs.players), nb_players)

        # no two players at the same place
        self.assertEqual(nb_players, len(set([p.spawn_position for p in gs.players])))

    def test_add_player_should_respect_orientation(self):
        gc = GameConfig(GameMap(20), spawn_positions=[Position(1, 1)], spawn_directions=[Direction(Direction.LEFT)])
        gs = GameState(gc, players=None)
        self.assertEqual(len(gs.players), 0)
        gs.add_player("Karl Marx")

        self.assertEqual(Direction(Direction.LEFT), gs.players[0].direction)

    def test_create_with_game_config(self):
        game_config = GameConfig.from_str("WWWW\nW 2W\nW 1W\nWWWW")
        gs = GameState(game_config)
        self.assertEqual(4, gs.game_map.size)
        self.assertEqual(2, len(gs.game_config.spawn_positions))

    def test_add_player_with_game_config(self):
        game_config = GameConfig.from_str("WWWW\nW 2W\nW 1W\nWWWW")
        gs = GameState(game_config)
        self.assertEqual(len(gs.players), 0)

        ps0 = gs.add_player("0")
        self.assertEqual(Position(2, 2), ps0.spawn_position)

        ps1 = gs.add_player("1")
        self.assertEqual(Position(2, 1), ps1.spawn_position)

        with self.assertRaises(Exception):
            gs.add_player("2")

    def test_is_closed_tail(self):
        # fmt: off
        gm = create_map_with([
            [1, E, 1],
            [E, E, E],
            [1, E, E]
        ])
        # fmt: on

        # player without tail
        player = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(player.tail, [Position(1, 1)])
        self.assertFalse(GameState.is_closed_tail(player, gm))

        # player with tail
        player.tail = [Position(1, 1), Position(2, 1)]
        self.assertFalse(GameState.is_closed_tail(player, gm))

        player.tail = [Position(1, 1), Position(2, 1), Position(3, 1)]
        player.direction = Direction(Direction.UP)
        self.assertTrue(GameState.is_closed_tail(player, gm))

        player.tail = [Position(1, 1), Position(2, 1), Position(2, 2)]
        self.assertFalse(GameState.is_closed_tail(player, gm))

        player.tail = [Position(1, 1), Position(2, 1), Position(2, 2), Position(1, 2), Position(1, 1)]
        self.assertTrue(GameState.is_closed_tail(player, gm))

    def test_respawn_player(self):
        gs = GameState(GameMap(5))
        player = gs.add_player("1")
        gs.move_player(player, Action.FORWARD)
        self.assertNotEqual(player.position, player.spawn_position)
        player.killed = True
        gs.respawn_player(player)
        self.assertEqual(player.position, player.spawn_position)
        self.assertFalse(player.killed)

    def test_move_player(self):
        gm = GameMap(5)
        player = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        player.direction = Direction(Direction.RIGHT)
        gs = GameState(gm, [player])
        gs.move_player(player, Action.FORWARD)
        gs.move_player(player, Action.TURN_RIGHT)
        gs.move_player(player, Action.TURN_RIGHT)
        gs.move_player(player, Action.TURN_LEFT)
        self.assertEqual(Position(1, 3), player.position)

    def test_kill_player(self):
        # fmt: off
        gm = create_map_with([
            [E, E, E],
            [E, E, E],
            [1, 1, 1]
        ])
        # fmt: on
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        gs = GameState(gm, [p1])

        p1.tail = [Position(1, 1), Position(1, 2)]
        p1.position = p1.tail[-1]
        gs.kill_player(p1)

        self.assertEqual(p1.tail, [p1.spawn_position])
        self.assertEqual(p1.position, p1.spawn_position)
        self.assertTrue(p1.killed)
        self.assertEqual(0, p1.stats.stats[PlayerStats.CONQUERED])

    def test_apply_action(self):
        gm = GameMap(5)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(1, p1.stats.stats[PlayerStats.CONQUERED])
        self.assertEqual(p1.direction, Direction.RIGHT)
        gs = GameState(gm, players=[p1])

        # go forward = ok
        gs.apply_action(1, p1, Action.FORWARD)
        self.assertEqual(p1.position, Position(2, 1))
        self.assertEqual(p1.tail, [Position(1, 1), Position(2, 1)])

        # turn left = go up = killed
        gs.apply_action(2, p1, Action.TURN_LEFT)
        self.assertEqual(p1.position, p1.spawn_position)
        self.assertEqual(p1.tail, [Position(1, 1)])
        self.assertTrue(p1.killed)
        self.assertEqual(1, p1.stats.stats[PlayerStats.SUICIDES])

        # next action is discarded
        gs.apply_action(3, p1, Action.FORWARD)
        self.assertEqual(p1.position, p1.spawn_position)
        self.assertEqual(p1.tail, [Position(1, 1)])
        self.assertFalse(p1.killed)

    def test_conquer(self):
        gm = GameMap(5)
        gm.conquer_tile(Position(2, 1), 1)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(p1.tail, [p1.spawn_position])
        self.assertTrue(gm.is_conquered_by(Position(1, 1), player_id=1))
        self.assertEqual(p1.direction, Direction.RIGHT)
        p1.stats.set_stat(PlayerStats.CONQUERED, gm.count_tiles_owned_by(player_id=1))

        gs = GameState(gm, players=[p1])

        # loop around
        gs.apply_action(1, p1, Action.FORWARD)
        self.assertEqual(p1.tail, [Position(2, 1)])

        gs.apply_action(2, p1, Action.TURN_RIGHT)
        self.assertEqual(p1.position, Position(2, 2))
        self.assertEqual(p1.tail, [Position(2, 1), Position(2, 2)])
        self.assertEqual(gm.count_tiles_owned_by(player_id=1), 2)
        self.assertEqual(2, p1.stats.stats[PlayerStats.CONQUERED])

        # walk into a conquered tile
        gs.apply_action(4, p1, Action.TURN_RIGHT)
        self.assertEqual(p1.position, Position(1, 2))
        self.assertEqual(p1.tail, [Position(2, 1), Position(2, 2), Position(1, 2)])

        gs.apply_action(1, p1, Action.TURN_RIGHT)
        self.assertEqual(p1.position, Position(1, 1))
        self.assertEqual(p1.tail, [Position(1, 1)])
        self.assertFalse(p1.killed)
        self.assertEqual(gm.count_tiles_owned_by(player_id=1), 4)
        self.assertEqual(4, p1.stats.stats[PlayerStats.CONQUERED])
        for p in [Position(1, 1), Position(2, 1), Position(2, 2), Position(1, 2)]:
            self.assertTrue(gm.is_conquered_by(p, player_id=1))

    def test_walk_on_tail_suicide(self):
        gm = GameMap(5)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(p1.direction, Direction.RIGHT)
        gs = GameState(gm, players=[p1])

        # loop around
        gs.apply_action(1, p1, Action.FORWARD)
        gs.apply_action(2, p1, Action.FORWARD)
        gs.apply_action(3, p1, Action.TURN_RIGHT)
        gs.apply_action(4, p1, Action.TURN_RIGHT)
        self.assertEqual(p1.position, Position(2, 2))
        self.assertEqual(p1.tail, [p1.spawn_position, Position(2, 1), Position(3, 1), Position(3, 2), Position(2, 2)])
        self.assertFalse(p1.killed)

        # walk on tail = suicide
        gs.apply_action(5, p1, Action.TURN_RIGHT)
        self.assertTrue(p1.killed)
        self.assertEqual(len(p1.tail), 1)
        self.assertEqual(1, p1.stats.stats[PlayerStats.SUICIDES])

    def test_walk_on_black_hole_suicide(self):
        gm = GameMap(5)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(p1.direction, Direction.RIGHT)
        gs = GameState(gm, players=[p1])
        gm.set_tile(Position(2, 1), GameMap.BLACK_HOLE)

        gs.apply_action(1, p1, Action.FORWARD)
        self.assertTrue(p1.killed)
        self.assertEqual(p1.position, Position(1, 1))
        self.assertEqual(len(p1.tail), 1)
        self.assertEqual(1, p1.stats.stats[PlayerStats.SUICIDES])

        if GameState.relocate_black_hole:
            self.assertFalse(gm.is_black_hole(Position(2, 1)))
            black_hole_at = None
            for y in range(gm.size):
                for x in range(gm.size):
                    pos = Position(x, y)
                    if gm.is_black_hole(pos):
                        black_hole_at = pos
            self.assertTrue(black_hole_at is not None)
        else:
            self.assertTrue(gm.is_black_hole(Position(2, 1)))

    def test_walk_on_blitzium(self):
        gm = GameMap(5)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(p1.direction, Direction.RIGHT)
        gs = GameState(gm, players=[p1])
        gm.set_tile(Position(2, 1), GameMap.BLITZIUM)

        gs.apply_action(1, p1, Action.FORWARD)
        self.assertFalse(p1.killed)
        self.assertEqual(p1.position, Position(2, 1))
        self.assertEqual(len(p1.tail), 2)
        self.assertEqual(1, p1.stats.stats[PlayerStats.BLITZIUMS])
        self.assertFalse(gm.is_blitzium(Position(2, 1)))

        if not GameState.relocate_blitzium:
            for y in range(gm.size):
                for x in range(gm.size):
                    self.assertFalse(gm.is_blitzium(Position(x, y)))

    def test_walk_on_tail_kill(self):
        # player 1 has some conquered tiles n the map
        # fmt: off
        gm = create_map_with([
            [E, E, E],
            [E, E, E],
            [1, 1, 1]
        ])
        # fmt: on
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        p2 = PlayerState(id=2, name="2", game_map=gm, position=Position(3, 2))
        gs = GameState(gm, players=[p1, p2])
        self.assertEqual(gm.count_tiles_owned_by(player_id=1), 4)
        self.assertEqual(gm.count_tiles_owned_by(player_id=2), 1)
        self.assertEqual(p1.direction, Direction.RIGHT)
        self.assertEqual(p2.direction, Direction.LEFT)

        # create some tail
        gs.apply_action(1, p1, Action.FORWARD)
        gs.apply_action(2, p1, Action.FORWARD)

        # p2 walk on p1 tail and kill it
        gs.apply_action(3, p2, Action.TURN_RIGHT)
        self.assertEqual(p2.position, Position(3, 1))
        self.assertTrue(p1.killed)
        self.assertEqual(gm.count_tiles_owned_by(player_id=1), 1)
        self.assertEqual(gm.count_tiles_owned_by(player_id=2), 1)
        self.assertEqual(1, p1.stats.stats[PlayerStats.KILLED])
        self.assertEqual(p2.name, p1.stats.stats[PlayerStats.NEMESIS])
        self.assertEqual(1, p2.stats.stats[PlayerStats.KILLS])

    def test_walk_on_asteroids_suicide(self):
        gm = GameMap(5)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        self.assertEqual(p1.direction, Direction.RIGHT)
        gs = GameState(gm, players=[p1])

        # validate that a turn left should walk on asteroids
        pos = p1.position.copy().move(Direction(Direction.RIGHT).change_direction(Action.TURN_LEFT))
        self.assertEqual(pos, Position(1, 0))
        self.assertTrue(gm.is_asteroids(pos))
        gs.apply_action(1, p1, Action.TURN_LEFT)

        # walk on tail = suicide, respawn
        self.assertEqual(p1.position, Position(1, 1))
        self.assertEqual(len(p1.tail), 1)
        self.assertTrue(p1.killed)
        self.assertEqual(1, p1.stats.stats[PlayerStats.SUICIDES])

    def test_surround_player_will_it(self):
        gm = GameMap(6)
        p1 = PlayerState(id=1, name="1", game_map=gm, position=Position(1, 1))
        p2 = PlayerState(id=2, name="2", game_map=gm, position=Position(2, 2))
        p3 = PlayerState(id=3, name="3", game_map=gm, position=Position(3, 3))
        p4 = PlayerState(id=4, name="3", game_map=gm, position=Position(4, 4))
        gs = GameState(gm, [p1, p2, p3, p4])
        gs.apply_action(0, p1, Action.FORWARD)
        gs.apply_action(0, p1, Action.FORWARD)
        gs.apply_action(0, p1, Action.TURN_RIGHT)
        gs.apply_action(0, p1, Action.FORWARD)
        gs.apply_action(0, p1, Action.TURN_RIGHT)
        gs.apply_action(0, p1, Action.FORWARD)
        gs.apply_action(0, p1, Action.TURN_RIGHT)
        gs.apply_action(0, p1, Action.FORWARD)
        self.assertEqual(9, p1.stats.stats[PlayerStats.CONQUERED])
        self.assertFalse(p1.killed)
        self.assertTrue(p2.killed)
        self.assertTrue(p3.killed)
        self.assertFalse(p4.killed)

    def test_fill_basic_1(self):
        # fmt: off
        game_map = create_map_with([
            [E, E, E, E, E],
            [E, 1, E, E, E],
            [E, 1, E, 1, E],
            [E, 1, 1, 1, E],
            [E, E, E, E, E]
        ])
        # fmt: on
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=Position(2, 2))
        ps.tail = [ps.spawn_position, Position(3, 2), Position(4, 2), Position(4, 3)]
        gs = GameState(game_map, [ps])
        self.assertEqual(len(gs.fill(ps)), 3)
        # fmt: off
        self.assertEqual(game_map, create_map_with([
            [E, E, E, E, E],
            [E, 1, 1, 1, E],
            [E, 1, 1, 1, E],
            [E, 1, 1, 1, E],
            [E, E, E, E, E]
        ]))
        # fmt: on
        self.assertEqual(ps.score, 3)

    def test_fill_basic_2(self):
        # fmt: off
        game_map = create_map_with([
            [E, 1, 1, E, E],
            [E, 1, 1, E, E],
            [E, E, E, E, E],
            [E, E, E, E, E],
            [E, E, E, E, E]
        ])
        # fmt: on
        ps = PlayerState(
            id=1, name="dummy", game_map=game_map, position=Position(2, 2), direction=Direction(Direction.DOWN)
        )
        gs = GameState(game_map, [ps])
        gs.apply_action(0, ps, Action.FORWARD)
        gs.apply_action(1, ps, Action.TURN_RIGHT)
        gs.apply_action(2, ps, Action.TURN_LEFT)
        gs.apply_action(3, ps, Action.TURN_LEFT)
        gs.apply_action(4, ps, Action.FORWARD)
        gs.apply_action(4, ps, Action.FORWARD)
        gs.apply_action(5, ps, Action.TURN_LEFT)
        gs.apply_action(6, ps, Action.FORWARD)
        gs.apply_action(7, ps, Action.TURN_LEFT)

        # fmt: off
        self.assertEqual(game_map, create_map_with([
            [E, 1, 1, E, E],
            [E, 1, 1, 1, E],
            [1, 1, 1, 1, E],
            [1, 1, 1, 1, E],
            [E, E, E, E, E]
        ]))
        # fmt: on
        self.assertEqual(ps.score, 9)

    def test_fill_with_asteroids(self):
        # fmt: off
        game_map = create_map_with([
            [E, E, E, E, E],
            [E, 1, E, 1, E],
            [E, 1, W, 1, E],
            [E, 1, 1, 1, E],
            [E, E, E, E, E]
        ])
        # fmt: on
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=Position(2, 2))
        ps.tail = [ps.spawn_position, Position(3, 2), Position(4, 2)]
        gs = GameState(game_map, [ps])
        self.assertEqual(len(gs.fill(ps)), 1)
        # fmt: off
        self.assertEqual(game_map, create_map_with([
            [E, E, E, E, E],
            [E, 1, 1, 1, E],
            [E, 1, W, 1, E],
            [E, 1, 1, 1, E],
            [E, E, E, E, E]
        ]))
        # fmt: on
        self.assertEqual(ps.score, 1)

    def test_fill_with_tail(self):
        # fmt: off
        game_map = create_map_with([
            [1, 1, 1, 1],
            [1, 1, E, 1],
            [E, E, E, E],
            [E, E, E, E]
        ])
        # fmt: on
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=Position(2, 2))
        gs = GameState(game_map, [ps])
        ps.tail = [ps.spawn_position, Position(2, 3), Position(3, 3), Position(4, 3), Position(4, 2)]
        self.assertEqual(len(gs.fill(ps)), 4)
        # fmt: off
        self.assertEqual(game_map, create_map_with([
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [E, 1, 1, 1],
            [E, E, E, E]
        ]))
        # fmt: on
        self.assertEqual(ps.score, 4)

    def test_fill_island(self):
        # fmt: off
        game_map = create_map_with([
            [1, 1, E, 1],
            [1, 1, E, 1],
            [E, E, E, E],
            [E, E, E, E]
        ])
        # fmt: on
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=Position(2, 2))
        gs = GameState(game_map, [ps])
        ps.tail = [ps.spawn_position, Position(2, 3), Position(3, 3), Position(4, 3), Position(4, 2)]
        self.assertEqual(len(gs.fill(ps)), 3)
        # fmt: off
        self.assertEqual(game_map, create_map_with([
            [1, 1, E, 1],
            [1, 1, E, 1],
            [E, 1, 1, 1],
            [E, E, E, E]
        ]))
        # fmt: on
        self.assertEqual(ps.score, 3)

    def test_fill_kill_other_player_tail(self):
        # fmt: off
        game_map = create_map_with([
            [E, E, E, E],
            [E, E, E, E],
            [0, 0, 0, 0],
            [E, 1, E, E]
        ])
        # fmt: on
        p0 = PlayerState(id=0, name="dummy", game_map=game_map, position=Position(1, 3))
        p1 = PlayerState(id=1, name="dummy", game_map=game_map, position=Position(2, 4))
        gs = GameState(game_map, [p0, p1])
        p0.tail = [
            p0.spawn_position.copy(),
            Position(1, 2),
            Position(1, 1),
            Position(2, 1),
            Position(3, 1),
            Position(4, 1),
            Position(4, 2),
        ]
        p0.position = p0.tail[-1].copy()
        p0.direction = Direction(Direction.DOWN)
        p1.tail = [
            p1.spawn_position.copy(),
            Position(2, 3),
            Position(2, 2),
            Position(3, 2),
            Position(3, 3),
            Position(3, 4),
        ]
        p1.position = p1.tail[-1].copy()
        p1.direction = Direction(Direction.DOWN)
        # print(game_state_to_dict(0, 0, gs, 999)['game']['pretty_map'])
        gs.apply_action(0, p0, Action.FORWARD)
        # print(game_state_to_dict(0, 0, gs, 999)['game']['pretty_map'])
        self.assertTrue(p1.killed)

    def test_fill_planet_to_planet_2(self):
        # fmt: off
        game_map = create_map_with([
            [E, E, E, P1, 1],
            [E, E, E, 1,  P1],
            [E, E, E, E,  E],
            [E, E, E, E,  E],
            [E, E, E, E,  E]
        ])
        # fmt: on
        ps = PlayerState(id=1, name="dummy", game_map=game_map, position=Position(4, 1))
        gs = GameState(game_map, [ps])
        ps.tail = [
            Position(4, 1),
            Position(3, 1),
            Position(2, 1),
            Position(2, 2),
            Position(2, 3),
            Position(2, 4),
            Position(3, 4),
            Position(4, 4),
            Position(5, 4),
            Position(5, 3),
            Position(5, 2),
        ]
        self.assertEqual(len(gs.fill(ps)), 12)
        # fmt: off
        self.assertEqual(game_map, create_map_with([
            [E, 1,  1, P1, 1],
            [E, 1,  1, 1,  P1],
            [E, 1,  1, 1,  1],
            [E, 1,  1, 1,  1],
            [E, E,  E, E,  E]
        ]))
        # fmt: on
        self.assertEqual(ps.score, 12)

    def test_relocate_item(self):
        # fmt: off
        gm = create_map_with([
            [1, E, E],
            [E, W, E],
            [E, E, E]
        ])
        # fmt: on
        ps = PlayerState(id=1, name="dummy", game_map=gm, position=Position(1, 1))
        gs = GameState(gm, [ps])
        ps.position = Position(3, 1)
        ps.tail = [Position(2, 1), Position(3, 1)]

        asteroids_pos = Position(2, 2)
        self.assertTrue(gm.is_asteroids(asteroids_pos))

        planet_pos = Position(3, 3)
        gm.set_tile(planet_pos, GameMap.PLANET)
        self.assertTrue(gm.is_planet(planet_pos))

        black_hole_pos = Position(1, 2)
        gm.set_tile(black_hole_pos, GameMap.BLACK_HOLE)
        self.assertTrue(gm.is_black_hole(black_hole_pos))

        blitzium_pos = Position(1, 3)
        gm.set_tile(blitzium_pos, GameMap.BLITZIUM)
        self.assertTrue(gm.is_blitzium(blitzium_pos))

        # Cannot relocate asteroids and planets
        with self.assertRaises(Exception):
            gs.relocate_item(asteroids_pos)
        with self.assertRaises(Exception):
            gs.relocate_item(planet_pos)

        # relocate black holes and blitziums
        for i in range(30):
            new_black_hole_pos = gs.relocate_item(black_hole_pos)
            self.assertTrue(
                new_black_hole_pos not in list({asteroids_pos, planet_pos, black_hole_pos, blitzium_pos}) + ps.tail
            )
            black_hole_pos = new_black_hole_pos

        new_blitzium_pos = gs.relocate_item(blitzium_pos)
        self.assertTrue(new_blitzium_pos != blitzium_pos)

    def test_relocate_item_map_full(self):
        # fmt: off
        gm = create_map_with([
            [E, W],
            [W, W]
        ])
        # fmt: on
        gs = GameState(gm, [])

        black_hole_pos = Position(1, 1)
        gm.set_tile(black_hole_pos, GameMap.BLACK_HOLE)
        self.assertTrue(gm.is_black_hole(black_hole_pos))

        new_black_hole_pos = gs.relocate_item(black_hole_pos)
        self.assertEqual(None, new_black_hole_pos)

    def test_respawn_on_someone_tail(self):
        gm = GameMap(5)
        p1 = PlayerState(id=1, name="p1", game_map=gm, position=Position(1, 1))
        p2 = PlayerState(id=2, name="p2", game_map=gm, position=Position(1, 2))
        gs = GameState(gm, [p1, p2])

        # p1: spawn position = 1,1, current position=3,1, tail [2,1 and 3,1]
        # p2: spawn position = 1,2, current position=2,2, tail [1,1, 1,2 and 2,2]
        p1.position = Position(3, 1)
        p1.tail = [Position(2, 1), Position(3, 1)]
        gm.set_tile(Position(1, 1), GameMap.EMPTY, 2)
        p2.position = Position(2, 2)
        p2.tail = [Position(1, 1), Position(1, 2), Position(2, 2)]
        p2.direction = Direction(Direction.UP)
        gs.apply_action(0, p2, Action.FORWARD)

        self.assertTrue(p1.killed)
        self.assertFalse(p2.killed)

        # respawn
        gs.respawn_player(p1)
        self.assertFalse(p1.killed)
        self.assertTrue(p2.killed)

    def test_conquer_player_last_tile(self):
        # fmt: off
        gm = create_map_with([
            [1, 1, E],
            [1, 2, E],
            [E, E, E],
        ])
        # fmt: on
        p1 = PlayerState(id=1, name="p1", game_map=gm, position=Position(1, 1))
        p2 = PlayerState(id=2, name="p2", game_map=gm, position=Position(2, 2))
        gs = GameState(gm, [p1, p2])

        p1.position = Position(2, 2)
        p1.tail = [Position(1, 2), Position(2, 2)]

        p2.position = Position(2, 3)
        p2.tail = [Position(2, 3)]

        p1.direction = Direction(Direction.RIGHT)
        gs.apply_action(0, p1, Action.TURN_LEFT)

        self.assertTrue(p2.killed)
        self.assertFalse(p1.killed)

    def test_conquer_some_player_tile(self):
        # fmt: off
        gm = create_map_with([
            [1, 1, E],
            [1, 2, 2],
            [E, 2, 2],
        ])
        # fmt: on
        p1 = PlayerState(id=1, name="p1", game_map=gm, position=Position(1, 1))
        p2 = PlayerState(id=2, name="p2", game_map=gm, position=Position(2, 2))
        gs = GameState(gm, [p1, p2])

        p1.position = Position(2, 2)
        p1.tail = [Position(1, 2), Position(2, 2)]

        p2.position = Position(2, 3)
        p2.tail = [Position(2, 3)]

        p1.direction = Direction(Direction.RIGHT)
        gs.apply_action(0, p1, Action.TURN_LEFT)

        self.assertFalse(p2.killed)
        self.assertFalse(p1.killed)

    def test_surround_player(self):
        # fmt: off
        gm = create_map_with([
            [1, 1, 1],
            [1, E, 1],
            [E, E, E],
        ])
        # fmt: on
        p1 = PlayerState(id=1, name="p1", game_map=gm, position=Position(1, 3), direction=Direction(Direction.RIGHT))
        p2 = PlayerState(id=2, name="p2", game_map=gm, position=Position(2, 2))
        gs = GameState(gm, [p1, p2])

        gs.apply_action(0, p1, Action.FORWARD)
        gs.apply_action(0, p1, Action.FORWARD)
        gs.apply_action(0, p1, Action.TURN_LEFT)

        self.assertTrue(p2.killed)
        self.assertFalse(p1.killed)

    def test_surround_player_with_conquers(self):
        # fmt: off
        gm = create_map_with([
            [1, 1, 1, E, E],
            [1, E, 1, E, E],
            [E, E, E, E, E],
            [E, E, E, 2, 2],
            [E, E, E, 2, 2],
        ])
        # fmt: on
        p1 = PlayerState(id=1, name="p1", game_map=gm, position=Position(1, 3), direction=Direction(Direction.RIGHT))
        p2 = PlayerState(id=2, name="p2", game_map=gm, position=Position(4, 4), direction=Direction(Direction.LEFT))
        gs = GameState(gm, [p1, p2])

        gs.apply_action(0, p2, Action.FORWARD)
        gs.apply_action(0, p2, Action.FORWARD)
        gs.apply_action(0, p2, Action.TURN_RIGHT)
        gs.apply_action(0, p2, Action.FORWARD)
        self.assertEqual(Position(2, 2), p2.position)
        self.assertEqual(5, len(p2.tail))

        gs.apply_action(0, p1, Action.FORWARD)  # walk on tail, p2 killed
        self.assertTrue(p2.killed)
        self.assertFalse(p1.killed)
        self.assertEqual(0, p2.stats.stats[PlayerStats.CONQUERED])

    def test_capturing_a_black_hole_suicide(self):
        # fmt: off
        gm = create_map_with([
            [0, 0, 0],
            [E, E, 0],
            [0, 0, 0]
        ])
        # fmt: on
        gm.set_tile(Position(2, 2), GameMap.BLACK_HOLE)
        p0 = PlayerState(id=0, name="p0", game_map=gm, position=Position(1, 1), direction=Direction(Direction.DOWN))
        gs = GameState(gm, [p0])
        gs.apply_action(0, p0, Action.FORWARD)
        self.assertFalse(p0.killed)
        gs.apply_action(0, p0, Action.FORWARD)
        self.assertTrue(p0.killed)
        self.assertEqual(1, p0.stats.stats[PlayerStats.SUICIDES])

    def test_capturing_a_blitzium(self):
        # fmt: off
        gm = create_map_with([
            [0, 0, 0],
            [E, E, 0],
            [0, 0, 0]
        ])
        # fmt: on
        gm.set_tile(Position(2, 2), GameMap.BLITZIUM)
        p0 = PlayerState(id=0, name="p0", game_map=gm, position=Position(1, 1), direction=Direction(Direction.DOWN))
        gs = GameState(gm, [p0])
        gs.apply_action(0, p0, Action.FORWARD)
        self.assertFalse(PlayerStats.BLITZIUMS in p0.stats.stats)
        gs.apply_action(0, p0, Action.FORWARD)
        self.assertFalse(p0.killed)
        self.assertEqual(1, p0.stats.stats[PlayerStats.BLITZIUMS])
