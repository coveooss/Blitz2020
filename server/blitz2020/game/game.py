import asyncio
import logging
import time
from asyncio import Future
from typing import List, Optional, Coroutine

from blitz2020.game.abstract_player import AbstractPlayer
from blitz2020.game.abstract_recorder import AbstractRecorder
from blitz2020.game.abstract_viewer import AbstractViewer
from blitz2020.game.action import Action
from blitz2020.game.game_state import GameState


class Game:
    def __init__(self, game_state: GameState, max_nb_ticks: int = 1000, move_timeout: int = 2, delay: int = 0):
        self.logger = logging.getLogger("Game")

        # Game state
        self.is_started = False
        self.game_tick = 0
        self.game_state = game_state
        self.players: List[AbstractPlayer] = []
        self.viewers: List[AbstractViewer] = []
        self.recorders: List[AbstractRecorder] = []

        # settings
        min_nb_ticks = 100
        self.max_nb_ticks = min(max_nb_ticks, max(min_nb_ticks, 16 * game_state.game_map.size + 70))
        self.move_timeout = move_timeout
        self.delay = delay

    def register_recorder(self, recorder: AbstractRecorder) -> None:
        self.logger.info(f"Recorder '{recorder.uid}' will record the game")
        self.recorders.append(recorder)

    def unregister_recorder(self, recorder: AbstractRecorder) -> None:
        self.logger.info(f"Recorder '{recorder.uid}' will stop recording the game")
        self.recorders.remove(recorder)

    def register_player(self, player: AbstractPlayer) -> AbstractPlayer:
        self.logger.info(f"Player '{player.name}' joined the game")

        # Create new player state
        new_player_state = self.game_state.add_player(player.name)
        player.set_player_state(new_player_state)

        self.logger.info(f"Player '{player.name}' => '{player.name_str()}': {player.player_state}'")
        self.players.append(player)

        return player

    def unregister_player(self, player: AbstractPlayer) -> None:
        self.logger.info(f"Player {player.name_str()} left the game")
        player.player_state.active = False
        self.is_started = (
            self.is_started and next(filter(lambda p: p.player_state.active, self.players), None) is not None
        )

    def register_viewer(self, viewer: AbstractViewer) -> None:
        self.logger.info(f"Viewer {viewer.uid} joined the game")
        self.viewers.append(viewer)

    def unregister_viewer(self, viewer: AbstractViewer) -> None:
        self.logger.info(f"Viewer {viewer.uid} disconnected")
        self.viewers.remove(viewer)

    async def game_loop(self) -> AbstractPlayer:
        self.is_started = True

        while self.is_started:
            self.game_tick += 1
            self.logger.info(f"Playing tick # {self.game_tick}")

            # respawn killed players before next move
            map(self.game_state.respawn_player, (p.player_state for p in self.players if p.player_state.killed))

            # Send game state to viewers.
            viewer_tasks: List[Coroutine] = [self.send_tick(viewer) for viewer in self.viewers]

            # Request next moves
            next_moves_tasks: List[Coroutine] = [self.request_next_move(p) for p in self.players]

            # wait for completion
            await asyncio.gather(*(next_moves_tasks + viewer_tasks), return_exceptions=True)

            # update player scores with conquered tiles
            self.game_state.update_players_scores()

            if self.game_tick >= self.max_nb_ticks:
                self.logger.info("!!! Game completed !!!")
                self.is_started = False

            [recorder.record_tick(self.game_tick, self.game_state) for recorder in self.recorders]

            # Time to slow things down
            if self.delay > 0:
                time.sleep(self.delay / 1000)

        self.players.sort(key=lambda x: x.player_state.score, reverse=True)
        for p in self.players:
            self.logger.info(f"Player '{p.name_str()}: {p.player_state}'")

        winner: AbstractPlayer = self.players[0]
        self.logger.info(f"... And the winner is: '{winner.name}':  {winner.player_state.score}")

        await asyncio.gather(*[self.send_winner(viewer, winner) for viewer in self.viewers], return_exceptions=True)

        [recorder.close() for recorder in self.recorders]

        return winner

    async def request_next_move(self, player: AbstractPlayer) -> Optional[Action]:
        player_action = None
        if player.player_state.active:
            # Do not request next move when a player was killed in the last turn
            if player.player_state.killed:
                self.logger.info(f"Player '{player.name_str()}' was killed. Skipping turn.")
            else:
                # Default action when something is wrong
                player_action = Action.FORWARD
                try:
                    # First turn, we leave more time to warm up everything.
                    true_timeout = 2 if self.game_tick == 0 else self.move_timeout
                    valid_move_for_tick = False
                    number_of_tries_left = 5

                    while not valid_move_for_tick and player.player_state.active and number_of_tries_left > 0:
                        number_of_tries_left -= 1

                        game_tick, player_action = await asyncio.wait_for(
                            player.request_next_move(self.game_tick, self.game_state), true_timeout
                        )

                        if game_tick != self.game_tick:
                            self.logger.warning(
                                f"Player '{player.name_str()}' returned an action for an out of sync game tick ({game_tick} != {self.game_tick})"
                            )
                            player.player_state.add_history(
                                self.game_tick,
                                f"Returned an action for an out of sync game tick ({game_tick} != {self.game_tick}).",
                            )
                            player_action = Action.FORWARD
                        else:
                            valid_move_for_tick = True
                except asyncio.TimeoutError:
                    self.logger.warning(f"Timeout while waiting for player '{player.name_str()}'.")
                    player.player_state.add_history(self.game_tick, "Timeout while waiting for player action.")
                except Exception as e:
                    self.logger.warning(f"Request next move for player '{player.name_str()}' failed with: '{e}'.")
                    player.player_state.add_history(self.game_tick, f"Request next move failed with: '{e}'.")

            self.logger.info(f"Applying '{player_action}' for player '{player.name_str()}'.")
            self.game_state.apply_action(self.game_tick, player.player_state, player_action)
            self.logger.debug(f"New player state for '{player.name_str()}': {player.player_state}.")

        return player_action

    async def send_tick(self, viewer: AbstractViewer) -> None:
        try:
            await asyncio.wait_for(viewer.send_tick(self.game_tick, self.game_state), self.move_timeout)
        except asyncio.TimeoutError:
            self.logger.warning(f"Timeout for viewer '{viewer.uid}'.")

    async def send_winner(self, viewer: AbstractViewer, winner: AbstractPlayer) -> None:
        try:
            await asyncio.wait_for(viewer.send_winner(self.game_tick, winner.player_state), self.move_timeout)
        except asyncio.TimeoutError:
            self.logger.warning(f"Timeout for viewer '{viewer.uid}'.")
