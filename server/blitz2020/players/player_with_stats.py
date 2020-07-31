from abc import abstractmethod

from blitz2020.game.abstract_player import AbstractPlayer


class PlayerWithStats(AbstractPlayer):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def print_stats(self) -> None:
        pass
