import json
import logging

import websockets

from blitz2020.game.abstract_viewer import AbstractViewer
from blitz2020.game.game_state import GameState
from blitz2020.game.player_state import PlayerState
from blitz2020.servers.abstract_server import AbstractServer
from blitz2020.servers.socket.utils import game_state_to_json, player_state_to_dict


class SocketViewer(AbstractViewer):
    def __init__(self, server: AbstractServer, websocket: websockets.WebSocketServerProtocol) -> None:
        super().__init__()
        self.logger = logging.getLogger("Viewer")
        self.server = server
        self.websocket = websocket

    async def close(self) -> None:
        await self.websocket.close()

    async def send_tick(self, game_tick: int, game_state: GameState) -> None:
        self.logger.info(f"{self.uid}: game_tick={game_tick}")

        tick = game_state_to_json(game_tick, -1, game_state, ticks_left=self.server.game.max_nb_ticks - game_tick)
        try:
            self.logger.info(f"{self.uid}: send tick to socket")
            await self.websocket.send(tick)

        except websockets.ConnectionClosed:
            self.logger.warning(f"Viewer '{self.uid}' disconnected.")
            self.server.game.unregister_viewer(self)

        except Exception as e:
            self.logger.warning(f"Error while processing viewer event: {e}")
            await self.close()
            self.server.game.unregister_viewer(self)

    async def send_winner(self, game_tick: int, player_state: PlayerState) -> None:
        self.logger.info(f"{self.uid}: winner={player_state.name_str()}")

        data = self.to_json(game_tick, player_state)
        try:
            self.logger.info(f"{self.uid}: send winner to socket")
            await self.websocket.send(data)

        except websockets.ConnectionClosed:
            self.logger.warning(f"Viewer '{self.uid}' disconnected.")
            self.server.game.unregister_viewer(self)

        except Exception as e:
            self.logger.warning(f"Error while processing viewer event: {e}")
            await self.close()
            self.server.game.unregister_viewer(self)

    def to_json(self, game_tick: int, winner: PlayerState) -> str:
        payload = {"type": "winner", "tick": game_tick, "winner": player_state_to_dict(winner)}
        return json.dumps(payload, indent=2)
