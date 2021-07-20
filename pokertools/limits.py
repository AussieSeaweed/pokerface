from abc import ABC, abstractmethod

from auxiliary import clip

from pokertools.gameframe import PokerPlayer


class Limit(ABC):
    """Limit is the abstract base class for all limits."""

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """Returns the game of this limit.

        :return: The game of this limit.
        """
        return self.__game

    @property
    def _min_amount(self):
        return min(max(map(PokerPlayer.bet.fget, self.game.players)) + self.game._max_delta, self.game.actor.total)

    @property
    def _pot_amount(self):
        return clip(self._pot_amount_raw, self._min_amount, self._max_amount)

    @property
    def _pot_amount_raw(self):
        bets = tuple(map(PokerPlayer.bet.fget, self.game.players))

        return 2 * max(bets) + sum(bets) - self.game.actor.bet + self.game.pot

    @property
    @abstractmethod
    def _max_amount(self): ...

    @property
    @abstractmethod
    def _max_count(self): ...


class FixedLimit(Limit):
    """FixedLimit is the class for fixed-limits."""

    @property
    def _max_amount(self):
        return self._min_amount

    @property
    def _max_count(self):
        return 4


class PotLimit(Limit):
    """PotLimit is the class for pot-limits."""

    @property
    def _max_amount(self):
        return clip(self._pot_amount_raw, self._min_amount, self.game.actor.total)

    @property
    def _max_count(self):
        return None


class NoLimit(Limit):
    """NoLimit is the class for no-limits."""

    @property
    def _max_amount(self):
        return self.game.actor.total

    @property
    def _max_count(self):
        return None
