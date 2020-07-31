import json
import logging
from typing import Tuple, Optional

import websockets
from blitz2020.game.abstract_player import AbstractPlayer
from blitz2020.game.action import Action
from blitz2020.game.game_state import GameState
from blitz2020.servers.abstract_server import AbstractServer
from blitz2020.servers.socket.utils import game_state_to_json


class SocketPlayer(AbstractPlayer):
    def __init__(self, server: AbstractServer, name: str, websocket: websockets.WebSocketServerProtocol) -> None:
        super().__init__(name)
        self.logger = logging.getLogger("SocketPlayer")
        self.server = server
        self.websocket = websocket

    async def close(self) -> None:
        await self.websocket.close()

    async def request_next_move_impl(self, game_tick: int, game_state: GameState) -> Tuple[Optional[int], Action]:
        self.logger.debug(f"{self.name_str()}: game_tick={game_tick}")

        action = Action.FORWARD
        received_tick = None
        tick = game_state_to_json(
            game_tick, self.player_state.id, game_state, ticks_left=self.server.game.max_nb_ticks - game_tick
        )

        try:
            self.logger.debug(f"{self.name_str()}: send tick to socket")
            await self.websocket.send(tick)

            self.logger.debug(f"{self.name_str()}: wait response on socket")
            message = await self.websocket.recv()

            self.logger.debug(f"{self.name_str()}: received response from socket: '{message!r}'")
            self.player_state.add_history(game_tick, f"Received response from socket: '{message!r}'")
            data = json.loads(message)

            try:
                if data["type"] != "move":
                    raise ValueError()

                action = Action[data["action"]]
                received_tick = data["tick"]

                self.logger.info(f"{self.name_str()}: action='{action}'")

            except:
                self.logger.warning(f"{self.name_str()}: invalid action: '{message!r}'")
                self.player_state.add_history(game_tick, "Invalid action")

        except websockets.ConnectionClosed:
            self.logger.warning(f"Player '{self.name_str()}' disconnected")
            self.server.game.unregister_player(self)

        except Exception as e:
            self.logger.warning(f"Error while processing player event: {e}")
            self.player_state.add_history(game_tick, f"Error while processing player event: {e}")

        return received_tick, action
