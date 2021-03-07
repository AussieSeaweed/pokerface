from abc import ABC
from collections.abc import Iterable, Iterator, MutableMapping
from itertools import chain, combinations, islice

from auxiliary import const, rotate, window
from math2.misc import product

from pokertools.cards import Card, Rank

PRIMES = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41


def mask(ranks: Iterable[Rank]) -> int:
    return product((PRIMES[rank.index] for rank in ranks), 1)


def straights(ranks: Iterable[Rank], count: int) -> Iterator[int]:
    keys = [mask(islice(rotate(sorted(ranks), -1), 0, count))]

    for sub_ranks in window(sorted(ranks), count):
        keys.append(mask(sub_ranks))

    return reversed(keys)


def multiples(ranks: Iterable[Rank], frequencies: MutableMapping[int, int]) -> Iterator[int]:
    if frequencies:
        ranks = frozenset(ranks)
        keys = []
        count = max(frequencies)
        frequency = frequencies.pop(count)

        for samples in combinations(sorted(ranks, reverse=True), frequency):
            key = mask(samples * count)
            ranks -= frozenset(samples)

            for sub_key in multiples(ranks, frequencies):
                keys.append(key * sub_key)

            ranks |= frozenset(samples)

        frequencies[count] = frequency
        return iter(keys)
    else:
        return iter((1,))


class Lookup(ABC):
    def __init__(self) -> None:
        self.suited_indices: MutableMapping[int, int] = {}
        self.unsuited_indices: MutableMapping[int, int] = {}
        self.index_count: int = 0

    def index(self, cards: Iterable[Card]) -> int:
        ranks, suits = zip(*((card.rank, card.suit) for card in cards))
        key = mask(ranks)

        try:
            if const(suits):
                return min(self.suited_indices[key], self.unsuited_indices[key])
            else:
                return self.unsuited_indices[key]
        except KeyError:
            raise ValueError('Cards do not form a valid hand')

    def register(self, indices: MutableMapping[int, int], key: int) -> None:
        if key not in indices:
            indices[key] = self.index_count
            self.index_count += 1


class StandardLookup(Lookup):
    def __init__(self) -> None:
        super().__init__()

        ranks = set(Rank)

        for key in straights(ranks, 5):
            self.register(self.suited_indices, key)

        for key in chain(multiples(ranks, {4: 1, 1: 1}), multiples(ranks, {3: 1, 2: 1})):
            self.register(self.unsuited_indices, key)

        for key in multiples(ranks, {1: 5}):
            self.register(self.suited_indices, key)

        for key in chain(straights(ranks, 5), multiples(ranks, {3: 1, 1: 2}), multiples(ranks, {2: 2, 1: 1}),
                         multiples(ranks, {2: 1, 1: 3}), multiples(ranks, {1: 5})):
            self.register(self.unsuited_indices, key)

    def index(self, cards: Iterable[Card]) -> int:
        return min(super(StandardLookup, self).index(combination) for combination in combinations(cards, 5))


class ShortLookup(Lookup):
    def __init__(self) -> None:
        super().__init__()

        ranks = set(rank for rank in Rank if Rank.FIVE < rank)

        for key in straights(ranks, 5):
            self.register(self.suited_indices, key)

        for key in multiples(ranks, {4: 1, 1: 1}):
            self.register(self.unsuited_indices, key)

        for key in multiples(ranks, {1: 5}):
            self.register(self.suited_indices, key)

        for key in chain(multiples(ranks, {3: 1, 2: 1}), straights(ranks, 5), multiples(ranks, {3: 1, 1: 2}),
                         multiples(ranks, {2: 2, 1: 1}), multiples(ranks, {2: 1, 1: 3}), multiples(ranks, {1: 5})):
            self.register(self.unsuited_indices, key)

    def index(self, cards: Iterable[Card]) -> int:
        return min(super(ShortLookup, self).index(combination) for combination in combinations(cards, 5))
