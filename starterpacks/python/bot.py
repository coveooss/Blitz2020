from typing import Dict, List
from game_message import *
from bot_message import *
import random


class Bot:

    def __init__(self):
        '''
        This method should be use to initialize some variables you will need throughout the game.
        '''

    def get_next_move(self, game_message: GameMessage) -> Move:
        '''
        Here is where the magic happens, for now the moves are random. I bet you can do better ;)
        '''
        players_by_id: Dict[int, Player] = game_message.generate_players_by_id_dict()

        legal_moves = self.get_legal_moves_for_current_tick(game=game_message.game, players_by_id=players_by_id)


        # You can print out a pretty version of the map but be aware that
        # printing out long strings can impact your bot performance (30 ms in average).
        # print(game_message.game.pretty_map)

        return random.choice(legal_moves)

    def get_legal_moves_for_current_tick(self, game: Game, players_by_id: Dict[int, Player]) -> List[Move]:
        '''
        You should define here what moves are legal for your current position and direction
        so that your bot does not send a lethal move.

        Your bot moves are relative to its direction, if you are in the DOWN direction.
        A TURN_RIGHT move will make your bot move left in the map visualization (replay or logs)
        '''
        me: Player = players_by_id[game.player_id]

        return [move for move in Move]
