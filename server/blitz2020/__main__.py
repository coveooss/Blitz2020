#!/usr/bin/env python
import asyncio
import json
import logging
import signal
import time
from pathlib import Path

import configargparse
from blitz2020.game.game_config import GameConfig
from blitz2020.servers.socket.socket_game_server import SocketGameServer

# We need that to shutdown the process on Windows (python ..)
signal.signal(signal.SIGINT, signal.SIG_DFL)

# CLI Argument parsing stuff
parser = configargparse.ArgumentParser(description="Blitz 2020 Game Server")
parser.add_argument(
    "--min_nb_players",
    env_var="MIN_NB_PLAYERS",
    help="Set a minimum number of players. The game will wait to reach that number before starting.",
    type=int,
    default=0,
)
parser.add_argument(
    "--max_nb_players",
    env_var="MAX_NB_PLAYERS",
    help="Set a maximum number of players. The game will refuse new players pass that number.",
    type=int,
    default=1000,
)
parser.add_argument(
    "--max_nb_ticks", env_var="MAX_NB_TICKS", help="Set a maximum number of game ticks.", type=int, default=500
)
parser.add_argument(
    "--log_level",
    env_var="LOG_LEVEL",
    help="Set the log level",
    type=str,
    default="INFO",
    choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
)
parser.add_argument(
    "--log_file", env_var="LOG_FILE", help="Set the file where logs should be outputted.", type=str, default=None
)
parser.add_argument(
    "--team_names_by_token",
    help="Set tokens for team registration",
    env_var="TEAM_NAMES_BY_TOKEN",
    type=str,
    default=None,
)
parser.add_argument("--game_config", env_var="GAME_CONFIG", help="Game setup config", type=str, default=None)
parser.add_argument(
    "--record_path", env_var="RECORD_PATH", help="Set a filename to save the game replay", type=str, default=None
)
parser.add_argument(
    "--s3_bucket", env_var="S3_BUCKET", help="Set the S3 Bucket name for game results", type=str, default=None
)

parser.add_argument("--s3_path", env_var="S3_PATH", help="Set the S3 path for the game results", type=str, default=None)

parser.add_argument(
    "--server_address",
    env_var="SERVER_ADDRESS",
    help="Set the address for the game server",
    type=str,
    default="localhost",
)

parser.add_argument(
    "--game_delay",
    env_var="GAME_DELAY",
    help="Allows you to slow down the game, useful for debuging. Value in (ms)",
    type=int,
    default=0,
)

parser.add_argument(
    "--move_timeout",
    env_var="MOVE_TIMEOUT",
    help="Allows you to specify the timeout for each turn. Useful when you want to be able to break in your bot. Value in (s)",
    type=int,
    default=0.300,
)  # 300 ms

parser.add_argument(
    "--start_delay_timeout",
    env_var="START_DELAY_TIMEOUT",
    help="Delay after which the game will start whether all players have registered or not",
    type=int,
    default=120,
)

args = parser.parse_args()

logFormatter = logging.Formatter("%(asctime)s - %(levelname)-8s [%(name)s] - %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(args.log_level)

if args.log_file:
    fileHandler = logging.FileHandler(args.log_file)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


async def start() -> None:
    # Start the game
    if args.game_config is not None:
        root_path = Path(__file__).parent.parent.parent
        file_path = (root_path / f"server/game_presets/{args.game_config}").resolve()
        game_config = GameConfig.from_file(file_path)

        game = SocketGameServer(
            max_nb_ticks=args.max_nb_ticks,
            min_nb_players=args.min_nb_players,
            max_nb_players=args.max_nb_players,
            start_delay_timeout=args.start_delay_timeout,
            team_names_by_token=json.loads(args.team_names_by_token) if args.team_names_by_token is not None else None,
            game_config=game_config,
            record_path=args.record_path,
            s3_bucket=args.s3_bucket,
            s3_path=args.s3_path,
            path=args.server_address,
            game_delay=args.game_delay,
            log_file=args.log_file,
            move_timeout=args.move_timeout,
        )
    else:
        game = SocketGameServer(
            max_nb_ticks=args.max_nb_ticks,
            min_nb_players=args.min_nb_players,
            max_nb_players=args.max_nb_players,
            start_delay_timeout=args.start_delay_timeout,
            team_names_by_token=json.loads(args.team_names_by_token) if args.team_names_by_token is not None else None,
            record_path=args.record_path,
            s3_bucket=args.s3_bucket,
            s3_path=args.s3_path,
            path=args.server_address,
            game_delay=args.game_delay,
            log_file=args.log_file,
            move_timeout=args.move_timeout,
        )

    await game.start()
    winner = await game.wait_for_game_to_finish()
    print(winner)
    print("\nSleeping a bit, to give a chance to the participant to upload their stuff.\n")
    time.sleep(2)


def main() -> None:
    asyncio.run(start())


if __name__ == "__main__":
    main()
