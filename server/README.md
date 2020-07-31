# Blitz 2020

Blitz 2020 game server

## Instructions

```
> python -m blitz2020 -h

usage: __main__.py [-h] [--min_nb_players MIN_NB_PLAYERS]
                   [--max_nb_players MAX_NB_PLAYERS]
                   [--log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]

optional arguments:
  -h, --help            show this help message and exit
  --min_nb_players MIN_NB_PLAYERS
                        Set a minimum number of players. The game will wait to
                        reach that number before starting.
  --max_nb_players MAX_NB_PLAYERS
                        Set a maximum number of players. The game will refuse
                        new players pass that number.
  --log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        Set the log level
```

### Tests

You can run tests using `python -m tests`. Tests are located in the `tests` folder.


Run coverage:
```
set PYTHONPATH=.
pytest --cov blitz2020 --cov tests --cov-report html 
```

# TODOs
### Game

- Predefined game configs: map asteroids setup, player spawn positions, goodies respawn probs
