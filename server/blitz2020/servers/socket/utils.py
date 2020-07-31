import json
from datetime import datetime
from typing import Optional, Dict, List, Tuple

import numpy
from blitz2020.game.direction import Direction
from blitz2020.game.game_map import GameMap
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState, HistoryItem
from blitz2020.game.player_stats import PlayerStats
from blitz2020.game.position import Position


def player_state_to_dict(p: PlayerState, with_history: bool = True) -> dict:
    data = {
        "active": p.active,
        "killed": p.killed,
        "position": {"x": p.position.x, "y": p.position.y},
        "spawn_position": {"x": p.spawn_position.x, "y": p.spawn_position.y},
        "direction": p.direction.to_string(),
        "spawn_direction": p.spawn_direction.to_string(),
        "tail": [{"x": t.x, "y": t.y} for t in p.tail],
        "id": p.id,
        "name": p.name,
        "score": p.score,
        "stats": {**p.stats.stats, "players_killed": p.stats.kills, "killed_by_players": p.stats.killed_by_players},
        "history": [
            {"timestamp": item.ts.isoformat(), "tick": item.tick, "message": item.message}
            for item in p.history
            if with_history
        ],
    }
    return data


def dict_to_position(data: Dict) -> Position:
    return Position(data["x"], data["y"])


def dict_to_player_stats(data: Dict) -> PlayerStats:
    ps = PlayerStats()
    for k, v in data.items():
        if k == "players_killed":
            ps.kills = v
        elif k == "killed_by_players":
            ps.killed_by_players = v
        else:
            ps.set_stat(k, v)
    return ps


def dict_to_player_state(data: Dict, game_map: GameMap) -> PlayerState:
    position = dict_to_position(data["position"])
    ps = PlayerState(id=data["id"], name=data["name"], game_map=game_map, position=position, init=False)
    ps.active = data["active"]
    ps.killed = data["killed"]
    ps.position = position
    ps.spawn_position = dict_to_position(data["spawn_position"])
    ps.direction = Direction(data["direction"])
    ps.spawn_direction = Direction(data["spawn_direction"])
    ps.tail = [dict_to_position(p) for p in data["tail"]]
    ps.score = data["score"]
    ps.stats = dict_to_player_stats(data["stats"])

    for hist in data["history"]:
        dt = datetime.fromisoformat(hist["timestamp"])
        ps.history.append(HistoryItem(game_tick=hist["tick"], message=hist["message"], ts=dt))

    return ps


def dict_to_game_map(data: List[List[str]]) -> GameMap:
    map_size = len(data)
    game_map = GameMap(map_size)

    for y in range(1, map_size - 1):
        for x in range(1, map_size - 1):
            splitted = data[y][x].split("-")
            tile = splitted[0]
            owner = None
            if len(splitted) > 1:
                owner = int(splitted[1])

            pos = Position(x, y)
            if tile == " ":
                game_map.set_tile(pos, GameMap.EMPTY, None)
            elif tile == "W":
                game_map.set_tile(pos, GameMap.ASTEROIDS, None)
            elif tile == "!":
                game_map.set_tile(pos, GameMap.BLACK_HOLE, None)
            elif tile == "$":
                game_map.set_tile(pos, GameMap.BLITZIUM, None)
            elif tile == "%":
                game_map.set_tile(pos, GameMap.PLANET, owner)
            elif tile == "C":
                game_map.set_tile(pos, GameMap.EMPTY, owner)

    return game_map


def game_state_to_dict(
    game_tick: int, player_id: Optional[int], game_state: GameState, ticks_left: int, with_history: bool = True
) -> dict:
    x_size = len(game_state.game_map.tiles[0])
    y_size = len(game_state.game_map.tiles)
    map = [["E"] * x_size for y in range(y_size)]
    for y in range(y_size):
        for x in range(x_size):
            tile, owner = game_state.game_map.tiles[y][x]
            if owner is not None:
                if tile == GameMap.EMPTY:
                    tile = "C"
                tile = f"{tile}-{owner}"
            map[y][x] = tile

    game_state_dict = {
        "type": "tick",
        "game": {
            "map": map,
            "pretty_map": generate_pretty_map_from_game_state(map, game_state),
            "player_id": player_id,
            "tick": game_tick,
            "ticks_left": ticks_left,
        },
        "players": [player_state_to_dict(p, with_history) for p in game_state.players],
    }

    return game_state_dict


def generate_pretty_map_from_game_state(map: List[List[str]], game_state: GameState) -> str:
    map_size = game_state.game_map.size
    pretty_map = [row.copy() for row in map]

    for y in range(len(pretty_map)):
        for x in range(len(pretty_map[0])):
            pretty_map[y][x] = pretty_map[y][x].strip()
            pretty_map[y][x] = pretty_map[y][x].replace("-", "")

    for player in game_state.players:
        y_position = player.position.y
        x_position = player.position.x
        player_id = str(player.id)

        for tail_tile in player.tail[:-1]:
            if "P" not in pretty_map[tail_tile.y][tail_tile.x]:
                pretty_map[tail_tile.y][tail_tile.x] += "T" + player_id

        pretty_map[y_position][x_position] += "P" + player_id

    pretty = numpy.array2string(numpy.array(pretty_map), max_line_width=map_size * 6 + 20, formatter={"all": "{:<5}".format}, threshold=map_size * map_size,)
    disclaimer = (
        "DISCLAMER: this map does not have the same content as the json game map. "
        "Symbols are combined to help you visualize every spot on this turn. Hyphen are also removed. "
        "See the documentation for the json map symbol signification."
        "\n"
        "Symbols added or modified on this map for visualization purpose are:"
        "\n"
        "Px: Position of player x - Cx: Conquered by player x - Tx: Tail of player x"
    )

    return f'{pretty}\n{disclaimer}'


def game_state_to_json(game_tick: int, player_id: Optional[int], game_state: GameState, ticks_left: int) -> str:
    tick_payload = game_state_to_dict(game_tick, player_id, game_state, ticks_left)
    return json.dumps(tick_payload, indent=2)


def dict_to_game_state(data: Dict) -> Tuple[int, GameState, int]:
    gm = dict_to_game_map(data["game"]["map"])
    players = [dict_to_player_state(p, gm) for p in data["players"]]
    gs = GameState(gm, players)
    gs.game_tick = data["game"]["tick"]
    return (data["game"]["player_id"], gs, data["game"]["ticks_left"])
