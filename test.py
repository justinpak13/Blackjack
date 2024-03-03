from Player import Player
from Deck import Deck
from collections import namedtuple
from strategies import basic_strategy

Card = namedtuple('Card', ['suit', 'rank'])


def test_get_value():
    deck = Deck(6)
    player = Player()
    card = deck.pop()
    player.add_card(card)
    print(card)
    card = deck.pop()
    print(card)
    player.add_card(card)
    card = deck.pop()
    player.add_card(card)
    print(card)
    print(player.get_hand_value())

def test_basic_strategy():
    deck = Deck(6)
    player = Player(1000)
    dealer = Player()

    card0 = Card("club", "10")
    card1 = Card("club", "2")

    card2 = Card("club", "A")
    card3 = Card("club", "Q")

    player.add_card(card0)
    player.add_card(card1)

    dealer.add_card(card2)
    dealer.add_card(card3)

    print(player.hand)
    print(dealer.hand)

    print(basic_strategy(player, dealer))



        

if __name__ == "__main__":
    test_basic_strategy()

