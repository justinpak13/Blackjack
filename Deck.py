from collections import namedtuple
from random import shuffle

Card = namedtuple('Card', ['suit', 'rank'])


class Deck:

    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suit = ['spade', 'club', 'heart', 'diamond']

    def __init__(self, number_of_decks: int):
        self._cards = [Card(suit, rank) for suit in self.suit for rank in self.ranks for i in range(number_of_decks)]
        shuffle(self._cards)
        self.number_of_decks = number_of_decks

    def __len__(self):
        return len(self._cards)

    def pop(self):
        return self._cards.pop()

    def reset_deck(self):
        self._cards = [Card(suit, rank) for suit in self.suit for rank in self.ranks for i in range(self.number_of_decks)]
        shuffle(self._cards)


if __name__ == "__main__":
    deck = Deck(6)
    print(len(deck))
