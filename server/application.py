#!/usr/bin/env python

import asyncio
import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict

import configargparse
import websockets
from blitz2020.game.action import Action as Move
from blitz2020.players.mcts_player_2 import MCTSPlayer2
from blitz2020.players.mcts_player_4 import MCTSPlayer4
from blitz2020.servers.socket.utils import dict_to_game_state
from dataclasses_json import dataclass_json


class MessageType(Enum):
    MOVE = "move"
    REGISTER = "register"


@dataclass_json
@dataclass
class BotMessage:
    type: MessageType
    action: Move = None
    tick: int = None
    token: str = None
    name: str = None


class Bot:
    def __init__(self, bot_name):
        self.bot = None
        if bot_name == "best-fast":
            self.bot = MCTSPlayer2(max_nb_ticks=9999, time_limit=10)
        elif bot_name == "MCTSPlayer4" or bot_name == "mlemay_best":
            self.bot = MCTSPlayer4(max_nb_ticks=9999)
        elif bot_name == "test":
            self.bot = MCTSPlayer4(max_nb_ticks=250, time_limit=500, max_look_ahead=5)

    async def get_next_move(self, state: Dict) -> Move:
        player_id, game_state, ticks_left = dict_to_game_state(state)
        self.bot.set_player_state(game_state.players[player_id])
        self.bot.max_nb_ticks = game_state.game_tick + ticks_left
        return await self.bot.request_next_move_impl(game_state.game_tick, game_state)


async def run(args):
    uri = "ws://127.0.0.1:8765"

    async with websockets.connect(uri) as websocket:
        bot = Bot(args.bot_name)
        if "TOKEN" in os.environ:
            await websocket.send(BotMessage(type=MessageType.REGISTER, token=os.environ["TOKEN"]).to_json())
        else:
            await websocket.send(BotMessage(type=MessageType.REGISTER, name=args.bot_name).to_json())

        await game_loop(websocket=websocket, bot=bot)


async def game_loop(websocket: websockets.WebSocketServerProtocol, bot: Bot):
    while True:
        try:
            message = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            # Connection is closed, the game is probably over
            break
        data = json.loads(message)

        next_move: Move = await bot.get_next_move(data)
        move_message = {"type": "move", "action": next_move.value}

        await websocket.send(BotMessage(type=MessageType.MOVE, action=next_move, tick=data["game"]["tick"]).to_json())

        await websocket.send(BotMessage(type=MessageType.MOVE, action=next_move, tick=data["game"]["tick"]).to_json())


if __name__ == "__main__":
    parser = configargparse.ArgumentParser(description="builtin bot")
    parser.add_argument("--bot_name", type=str, default="best-fast")
    args = parser.parse_args()
    print(f"Selecting bot: {args.bot_name}")

    asyncio.get_event_loop().run_until_complete(run(args))
