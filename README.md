# Blitz 2020

## Instructions

See [server/README.md](server/README.md) and [ui/README.md](ui/README.md) specific instructions.

## Protocol

The game uses WebSockets to interact with the different bots on port 8765. The bot first need to register itself. After that, it will receive "ticks" containing the game data and will have to respond with a move command.

### Register

The first step is to register your bot. The payload should contain a `type` and a `name`. All payloads are JSON formatted.

```json
{ "type": "register", "name": "[YOUR TEAM NAME]" }
```

### Ticks

Each turn, the server will send you game data. The game data is composed of the map, the other players information and current game information.

```json
{
  "type": "tick",
  "players": [
    {
      "id": 0,
      "active": true,
      "killed": false,
      "position": { "x": 1, "y": 4 },
      "spawn_position": { "x": 1, "y": 1 },
      "tail": [{ "x": 1, "y": 1 }, { "x": 1, "y": 2 }, { "x": 1, "y": 3 }],
      "direction": "UP",
      "score": 0,
      "name": "[BOT NAME]",
      "stats": {
          "number_of_captured_tiles": 1,
          "number_of_kills": 1,
          "number_of_deaths": 1,
          "number_of_suicides": 1,
          "nemesis_player": "[OTHER BOT NAME]",
          "players_killed": {"[OTHER BOT NAME]": 1},
          "killed_by_players": {"[OTHER BOT NAME]": 1}
        },
        "history": [
            {"timestamp": "1900-01-01T13:14:15.000555", "tick": 11, "message": "message-11"},
            {"timestamp": "1900-01-01T13:14:15.000444", "tick": 10, "message": "message-10"}
        ]
    },
    {
    ...
    }
  ],
  "game": {
    "player_id": 0,
    "tick": 150,
    "ticks_left": 250,
    "map": [["E", "E", "E"], ["E", "E", "E"], ["E", "E", "E"]]
  }
}
```

### Move

After each tick, you are expected to send a move action (can be `FORWARD`, `TURN_LEFT`, `TURN_RIGHT`).

```json
{ "type": "move", "action": "TURN_LEFT" }
```

##Game rules

- Game rules:
  * Walking on someone's tail kill him (or suicide if it is player own tail)
  * Walking on a wall commits suicide.
  * When a player is killed, he loses all it's captured tiles and is respawned at starting position 

- Captures:
  * To capture tiles, a player must walk to any tile adjacent to a tile he currently owns
  * Capturing a player current position kills it

- Scoring rules:
  * Newly captured tiles = 1 point per tile
  * Killing a player reward 50 points
  * At the end of each turn, 0.2 point per captured tiles

Walls: 
  * non walkable tiles, not ownable tiles.. 
 
Goodies:
- Planets: more points when while captured
- Blitzium: walk on it = capture, capture tiles get it..  respawn randomly
- Black holes: walk on it = kill, respawn