from unittest import TestCase, main

from pokertools import FixedLimitFiveCardOmahaHoldEm, PotLimitFiveCardOmahaHoldEm
from pokertools.tests import PokerTestCaseMixin


class FixedLimitFiveCardOmahaHoldEmTestCase(PokerTestCaseMixin, TestCase):
    GAME_TYPE = FixedLimitFiveCardOmahaHoldEm

    def test_hands(self):
        ...  # TODO


class PotLimitFiveCardOmahaHoldEmTestCase(PokerTestCaseMixin, TestCase):
    GAME_TYPE = PotLimitFiveCardOmahaHoldEm

    def test_hands(self):
        ...  # TODO


if __name__ == '__main__':
    main()
