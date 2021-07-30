from os.path import exists
from pathlib import Path
from unittest import TestCase, main, skipUnless

from pokertools import BadugiHand, LowballA5Hand, ShortDeckHand, StandardHand, parse_cards

TEST_DIR = Path(__file__).parent / 'lookups'


class LookupTestCase(TestCase):
    @skipUnless(
        exists(TEST_DIR / 'lowballA5-lookup.txt'),
        'lowballA5 hand file not found',
    )
    def test_lowballA5_lookup(self):
        with open(TEST_DIR / 'lowballA5-lookup.txt') as file:
            lines = map(str.strip, file.readlines())

        indices = tuple(map(LowballA5Hand._lookup.get_index, map(
            parse_cards, lines,
        )))

        for i, j in zip(indices, indices[1:]):
            self.assertGreaterEqual(i, j)

        self.assertEqual(LowballA5Hand._lookup.index_count, 6175)
        self.assertEqual(min(indices), 0)
        self.assertEqual(max(indices), LowballA5Hand._lookup.index_count - 1)

    @skipUnless(
        exists(TEST_DIR / 'badugi-lookup.txt'),
        'badugi hand file not found',
    )
    def test_badugi_lookup(self):
        with open(TEST_DIR / 'badugi-lookup.txt') as file:
            lines = map(str.strip, file.readlines())

        indices = tuple(map(BadugiHand._lookup.get_index, map(
            parse_cards, lines,
        )))

        for i, j in zip(indices, indices[1:]):
            self.assertGreaterEqual(i, j)

        self.assertEqual(BadugiHand._lookup.index_count, 1092)
        self.assertEqual(min(indices), 0)
        self.assertEqual(max(indices), BadugiHand._lookup.index_count - 1)

    @skipUnless(
        exists(TEST_DIR / 'standard-lookup.txt'),
        'standard hand file not found',
    )
    def test_standard_lookup(self):
        # Generated by: https://pypi.org/project/treys/.
        with open(TEST_DIR / 'standard-lookup.txt') as file:
            lines = map(str.strip, file.readlines())

        indices = tuple(map(StandardHand._lookup.get_index, map(
            parse_cards, lines,
        )))

        for i, j in zip(indices, indices[1:]):
            self.assertLessEqual(i, j)

        self.assertEqual(StandardHand._lookup.index_count, 7462)
        self.assertEqual(min(indices), 0)
        self.assertEqual(max(indices), StandardHand._lookup.index_count - 1)

    @skipUnless(
        exists(TEST_DIR / 'short-hand-lookup.txt'),
        'short hand file not found',
    )
    def test_short_deck_lookup(self):
        # Generated by: https://github.com/amason13/shortdeck.
        with open(TEST_DIR / 'short-hand-lookup.txt') as file:
            lines = map(str.strip, file.readlines())

        indices = tuple(map(ShortDeckHand._lookup.get_index, map(
            parse_cards, lines,
        )))

        for i, j in zip(indices, indices[1:]):
            self.assertLessEqual(i, j)

        self.assertEqual(ShortDeckHand._lookup.index_count, 1404)
        self.assertEqual(min(indices), 0)
        self.assertEqual(max(indices), ShortDeckHand._lookup.index_count - 1)


if __name__ == '__main__':
    main()
