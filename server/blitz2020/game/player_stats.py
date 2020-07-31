import json
from typing import Dict, Any


class PlayerStats:
    # counted statistics
    KILLS = "number_of_kills"
    KILLED = "number_of_deaths"
    SUICIDES = "number_of_suicides"
    PLANETS = "number_of_planets_conquered"
    BLITZIUMS = "number_of_blitziums_collected"
    CONQUERED = "number_of_conquered_tiles"
    counted_stats = {KILLS, KILLED, SUICIDES, PLANETS, BLITZIUMS, CONQUERED}

    # other values
    NEMESIS = "nemesis_player"

    def __init__(
        self, stats: Dict[str, Any] = None, kills: Dict[str, int] = None, killed_by_players: Dict[str, int] = None
    ):
        if stats is None:
            self.stats = {}
        else:
            self.stats = stats

        if kills is None:
            self.kills = {}
        else:
            self.kills = kills

        if killed_by_players is None:
            self.killed_by_players = {}
        else:
            self.killed_by_players = killed_by_players

    def __str__(self) -> str:
        stats = {**self.stats, "players_killed": self.kills, "killed_by_players": self.killed_by_players}
        return json.dumps(stats)

    def add_stat(self, stat: str) -> None:
        assert stat in PlayerStats.counted_stats
        self.stats[stat] = self.stats.setdefault(stat, 0) + 1

    def set_stat(self, stat: str, value: Any) -> None:
        assert stat not in PlayerStats.counted_stats or isinstance(value, int)
        self.stats[stat] = value

    def kill_player(self, player: str) -> None:
        assert len(player) > 0
        self.add_stat(PlayerStats.KILLS)
        self.kills[player] = self.kills.setdefault(player, 0) + 1

    def killed_by_player(self, player: str) -> None:
        assert len(player) > 0
        self.add_stat(PlayerStats.KILLED)
        self.killed_by_players[player] = self.killed_by_players.setdefault(player, 0) + 1
        nemesis: str = max(self.killed_by_players.items(), key=lambda x: x[1])[0]
        self.set_stat(PlayerStats.NEMESIS, nemesis)

    def safe_get(self, stat_name: str) -> Any:
        if stat_name in self.stats:
            return self.stats[stat_name]
        else:
            return 0
