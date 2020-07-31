import copy
import logging
import random
from typing import List, Optional, Set, Union, Dict

from blitz2020.game.action import Action
from blitz2020.game.flood import flood
from blitz2020.game.game_config import GameConfig
from blitz2020.game.game_map import GameMap
from blitz2020.game.player_state import PlayerState
from blitz2020.game.player_stats import PlayerStats
from blitz2020.game.position import Position

logger = logging.getLogger("GameState")


class GameState:
    SCORE_NEW_CONQUERED = 1.0
    SCORE_CONQUERED = 0.02
    SCORE_CONQUERED_PLANET = 0.5
    SCORE_CAPTURED_BLITZIUM = 50
    SCORE_TAIL = 0.0  # Disabled for now
    SCORE_KILL_PLAYER = 50

    relocate_black_hole = False
    relocate_blitzium = False

    def __init__(self, game_config: Union[GameConfig, GameMap], players: List[PlayerState] = None):
        self.logger = logger

        if isinstance(game_config, GameConfig):
            self.game_map: GameMap = game_config.game_map
            self.game_config: Optional[GameConfig] = game_config
        elif isinstance(game_config, GameMap):
            self.game_map = game_config
            self.game_config = None
        else:
            raise Exception(f"Invalid argument {game_config}")

        if players is None:
            players = []
        self.players = players
        self.game_tick = 0

    def __deepcopy__(self, memodict: Dict) -> "GameState":
        gm = copy.deepcopy(self.game_map, memodict)
        obj = type(self)(gm)
        obj.game_tick = self.game_tick
        obj.players = [p.__deepcopy__(memodict) for p in self.players]
        return obj

    def add_player(self, name: str) -> PlayerState:
        id = len(self.players)

        spawn_position = None  # random position
        spawn_direction = None  # random orientation
        if self.game_config is not None:
            # will throw if out of bound
            if len(self.game_config.spawn_positions) > 0:
                spawn_position = self.game_config.spawn_positions[id]
            if len(self.game_config.spawn_directions) > 0:
                spawn_direction = self.game_config.spawn_directions[id]

        player = PlayerState(
            id=id, name=name, game_map=self.game_map, position=spawn_position, direction=spawn_direction
        )
        self.players.append(player)

        return player

    def apply_action(self, game_tick: int, player: PlayerState, action: Optional[Action]) -> None:
        self.game_tick = game_tick
        if player.killed:
            msg = f"Player '{player.name_str()}' was killed in the last turn, skip current action."
            self.logger.info(msg)
            player.add_history(game_tick, msg)

            # Respawn a player after killed
            self.respawn_player(player)
        else:
            # Change direction and move
            self.move_player(player, action)

            # If you move outside the map or an asteroids; you die.
            if self.game_map.is_out_of_bound(player.position) or self.game_map.is_asteroids(player.position):
                self.logger.info(f"Player '{player.name_str()}' stepped on an asteroids or outside the map.")
                player.stats.add_stat(PlayerStats.SUICIDES)
                player.add_history(game_tick, f"Committed suicide by going out of bound.")
                self.kill_player(player)
            elif not self.stepped_on_a_black_hole(player.position, player):
                # Are we about to kill a player ?
                poor_player = self.will_kill_player(player)
                if poor_player != None:
                    self.kill_player_by(poor_player, player)

                if not player.killed:
                    # check if player captured a blitzium
                    self.check_if_captured_a_blitzium(player.position, player)

                    # Check if player conquered a territory
                    if GameState.is_closed_tail(player, self.game_map):
                        tilesOwnedBeforeConquere = dict()
                        for p in self.players:
                            tilesOwnedBeforeConquere[p.id] = self.game_map.count_tiles_owned_by(p.id)

                        new_conquers: Set[Position] = self.fill(player)

                        for p in self.players:
                            # check if we conquered current position of a player
                            # if p.id != player.id and (p.position in new_conquers or p.tail[0] in new_conquers):
                            if p.id != player.id and len(set(p.tail) & new_conquers) > 0:
                                self.kill_player_by(p, player)
                            # check if we conquered the last owned tiles of a player
                            if (
                                p.id != player.id
                                and tilesOwnedBeforeConquere[p.id] != 0
                                and self.game_map.count_tiles_owned_by(p.id) == 0
                            ):
                                self.kill_player_by(p, player)

    def respawn_player(self, player: PlayerState) -> None:
        # discard current action
        msg = f"Respawning player '{player.name_str()}'."
        self.logger.info(msg)
        player.add_history(self.game_tick, msg)
        player.killed = False
        player.reset_position()

        # check if it kill another player
        poor_player = self.will_kill_player(player)
        if poor_player is not None:
            self.kill_player_by(poor_player, player)

    def move_player(self, player: PlayerState, action: Action) -> None:
        prev_position = player.position.copy()
        prev_direction = player.direction.copy()

        player.direction.change_direction(action)
        player.position.move(player.direction)

        self.logger.info(f"Player '{player.name_str()}' moving to position: {player.position}.")
        player.add_history(
            self.game_tick,
            f"Moving {action.value} from {prev_position}-{prev_direction.name()} to {player.position}-{player.direction.name()}.",
        )

        # Append tail if:
        # - currently on an empty (or other player) tile
        # - walking on a captured tile and have non captured tiles in the tail
        if not self.game_map.is_conquered_by(player.position, player.id) or not self.game_map.is_conquered_by(
            player.tail[-1], player.id
        ):
            self.logger.debug(f"Player '{player.name_str()}' appending position to tail.")
            player.tail.append(player.position.copy())
        else:
            player.tail = [player.position.copy()]

    def kill_player(self, poor_player: PlayerState) -> None:
        self.game_map.clear_tile_owned_by(poor_player.id)
        poor_player.reset_position()
        poor_player.killed = True
        poor_player.stats.set_stat(PlayerStats.CONQUERED, 0)

    def kill_player_by(self, poor_player: PlayerState, player: PlayerState) -> None:
        if poor_player.id != player.id:
            self.logger.info(f"Player '{player.name_str()}' will kill player '{poor_player.name_str()}'.")
            player.score += GameState.SCORE_KILL_PLAYER
            player.stats.kill_player(poor_player.name)
            poor_player.stats.killed_by_player(player.name)
            player.add_history(self.game_tick, f"Killed player '{poor_player.name}'")
        else:
            self.logger.info(f"Player '{player.name_str()}' committed suicide!.")
            player.stats.add_stat(PlayerStats.SUICIDES)
            player.add_history(self.game_tick, f"Committed suicide by walking on player tail.")

        self.kill_player(poor_player)

    def will_kill_player(self, player: PlayerState) -> Optional[PlayerState]:
        # A player can kill itself if it walks on it's tail.
        for p in self.players:
            # Do not consider current player position when checking if walking on self tail
            if p.id == player.id:
                player_tail = p.tail[1:-1]
            else:
                player_tail = p.tail

            if player.position in player_tail:
                return p
        return None

    def fill(self, player: PlayerState) -> Set[Position]:
        id = player.id

        # tail have the starting and ending tiles (last tile before going in the empty zone and first captured tile)
        assert len(player.tail) >= 3
        assert self.game_map.is_conquered_by(player.tail[0], id)
        assert self.game_map.is_conquered_by(player.tail[-1], id)

        # new captured tiles minus start and end tiles (already captured)
        new_conquers = set(player.tail[1:-1])

        # check if we have a closed loop to fill: find shortest path from start to end of tail while walking only on conquered tiles
        closed_loop, shortest_path_to_close_tail = self.game_map.find_path(player.tail[0], player.tail[-1], id)
        if closed_loop:
            # Conquer the closed shape made by the tail
            map_size = self.game_map.size
            flooded_tiles = [[1] * map_size for _ in range(map_size)]

            for p in player.tail:
                flooded_tiles[p.y][p.x] = 0
            for p in shortest_path_to_close_tail:
                flooded_tiles[p.y][p.x] = 0

            # flooding work by changing the value to 0 for every reachable tiles from the top left of the map (skipping bombs,
            # walls and other players)  The remainder are the tiles that will be flooded. Using the closest path from start
            # to end of the tail make sure that we are filling only the smallest zone  when wrap around and also make sure we
            # do not re-kill any players walking inside our captured zone.
            flood(flooded_tiles, target=1, replacement=0)

            for y in range(map_size):
                for x in range(map_size):
                    if flooded_tiles[y][x] == 1:
                        p = Position(x, y)

                        # skip already conquered tiles or walls (asteroids)
                        if not self.game_map.is_conquered_by(p, id) and not self.game_map.is_asteroids(p):
                            if self.game_map.is_black_hole(p):
                                # if we happen to surround a black hole, we die instantly
                                self.stepped_on_a_black_hole(p, player)
                                return set()

            for y in range(map_size):
                for x in range(map_size):
                    if flooded_tiles[y][x] == 1:
                        p = Position(x, y)

                        # skip already conquered tiles or walls (asteroids)
                        if not self.game_map.is_conquered_by(p, id) and not self.game_map.is_asteroids(p):
                            if self.game_map.is_blitzium(p):
                                # surrounding a coin (blitzium) will give us more points.
                                self.check_if_captured_a_blitzium(p, player)

                            # add tile to new conquered tiles for later scoring
                            new_conquers.add(p)
                            self.game_map.conquer_tile(p, id)

        # capture the tail (no-op to recapture start and end tiles)
        for t in player.tail:
            self.game_map.conquer_tile(t, id)
        player.tail = [player.position.copy()]

        # adjust stats
        nb_conquers = len(new_conquers)
        self.logger.info(f"Player '{player.name_str()}' is capturing {nb_conquers} new tiles..")
        player.stats.set_stat(PlayerStats.CONQUERED, player.stats.stats[PlayerStats.CONQUERED] + nb_conquers)
        player.score += GameState.SCORE_NEW_CONQUERED * nb_conquers
        player.add_history(self.game_tick, f"Conquered {nb_conquers} new tiles.")
        return new_conquers

    def update_players_scores(self) -> None:
        # tiles count may become out of sync because a player might conquer someone else territory
        for player in self.players:
            player.stats.set_stat(PlayerStats.CONQUERED, 0)
            player.stats.set_stat(PlayerStats.PLANETS, 0)

        for x in range(0, self.game_map.size):
            for y in range(0, self.game_map.size):
                tile_state, player_id = self.game_map.get_tile(Position(x, y))

                if player_id is not None:
                    if tile_state == GameMap.PLANET:
                        self.players[player_id].score += GameState.SCORE_CONQUERED_PLANET
                        self.players[player_id].stats.add_stat(PlayerStats.PLANETS)
                    else:
                        self.players[player_id].score += GameState.SCORE_CONQUERED

                    self.players[player_id].stats.add_stat(PlayerStats.CONQUERED)

        for p in self.players:
            p.score += len(p.tail) * GameState.SCORE_TAIL

    @classmethod
    def is_closed_tail(cls, player: PlayerState, game_map: GameMap) -> bool:
        # check if adjacent to a conquered node
        if len(player.tail) >= 3:
            return game_map.is_conquered_by(player.tail[-1], player.id)
        return False

    def stepped_on_a_black_hole(self, pos: Position, player: PlayerState) -> bool:
        if self.game_map.is_black_hole(pos):
            self.logger.info(f"Player '{player.name_str()}' stepped on a black hole.")
            player.stats.add_stat(PlayerStats.SUICIDES)
            player.add_history(self.game_tick, f"Committed suicide by stepping on a black hole.")
            self.kill_player(player)
            if GameState.relocate_black_hole:
                self.relocate_item(pos)
            # permanent black_hole else: self.game_map.clear_tile(pos)
        return player.killed

    def check_if_captured_a_blitzium(self, pos: Position, player: PlayerState) -> None:
        if self.game_map.is_blitzium(pos):
            self.logger.info(f"Player '{player.name_str()}' found a blitzium.")
            player.stats.add_stat(PlayerStats.BLITZIUMS)
            player.add_history(self.game_tick, "Found a blitzium.")
            player.score += GameState.SCORE_CAPTURED_BLITZIUM
            if GameState.relocate_blitzium:
                self.relocate_item(pos)
            else:
                self.game_map.clear_tile(pos)

    def relocate_item(self, pos: Position) -> Optional[Position]:
        tile, _ = self.game_map.get_tile(pos)
        if tile != GameMap.BLACK_HOLE and tile != GameMap.BLITZIUM:
            raise Exception(f"Cannot relocate {tile}.")

        empty_tiles = set(self.game_map.get_empty_tiles())

        # cannot relocate on a player tail
        for p in self.players:
            for tail in p.tail:
                if tail in empty_tiles:
                    empty_tiles.remove(tail)

        self.game_map.clear_tile(pos)

        if len(empty_tiles) > 0:
            new_pos: Position = random.choice(tuple(empty_tiles))
            self.game_map.set_tile(new_pos, tile, None)
            self.logger.info(f"Moving {tile} to position {new_pos}.")

            return new_pos
        else:
            self.logger.info(f"Cannot move {tile} because there is no empty tile.")
            return None
