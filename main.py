from Deck import Deck
from Player import Player
from strategies import dealer_strategy
from strategies import basic_strategy
from strategies import card_counting
from random import randint
from Choices import choices
from collections import namedtuple
import numpy as np 
from matplotlib import pyplot as plt
import math
import pandas as pd

Card = namedtuple('Card', ['suit', 'rank'])

MIN_BET_AMOUNT = 25
PLAYER_AMOUNT = 500
TOTAL_GAMES = 100

CARD_COUNTING = True
RANDOM_BETTING = False
MIN_BETTING = False

BASIC_STRATEGY = True

def main():
    deck = Deck(6)
    player = Player(PLAYER_AMOUNT)
    dealer = Player()
    number_to_switch = randint(60, 75)
    card_count_dict = {}

    
    player_wins = 0
    games_played = 0

    for i in range(TOTAL_GAMES):
        if player.money < MIN_BET_AMOUNT:
            break

        player.clear_hand()
        dealer.clear_hand()

        if len(deck) < number_to_switch:
            number_to_switch = randint(60, 75)
            deck.reset_deck()
            card_count_dict = {}

        

        result = game(deck, player, dealer, card_count_dict)
        if result == 1:
            print("Player wins")
            player_wins += 1
        if result == -1:
            print("Dealer wins")
        if result == 0:
            print("Tie")

        games_played += 1

        print(f"Player Hand({player.get_hand_value()}): {player.hand}")
        print(f"Dealer Hand({dealer.get_hand_value()}): {dealer.hand}")

        print(f"Player has ${player.money}.00\n\n")

    print(f"Winning Percentage:{player_wins / games_played * 100}%")
    print(f"Winning Games: {player_wins}")
    print(f"Total Games: {games_played}")

    return player.money


def game(deck: Deck, player: Player, dealer: Player, card_count_dict: dict):

    # need to add ability to change bet amount
    # currently random amount between 25 and 100%
    if MIN_BETTING:
        bet_amount = MIN_BET_AMOUNT
    elif RANDOM_BETTING:
        bet_amount = max(round(player.money * randint(25,50) / 100), MIN_BET_AMOUNT)
    elif CARD_COUNTING:
        bet_amount = max(round(MIN_BET_AMOUNT * card_counting(card_count_dict)), MIN_BET_AMOUNT)

    player.bet(bet_amount)


    for i in range(2):
        dealer.add_card(deck.pop())
        player.add_card(deck.pop())


    # checks for naturals from both player and dealer
    if dealer.natural():
        if player.natural():
            player.add_money(bet_amount)
            dealer.add_to_count(card_count_dict)
            player.add_to_count(card_count_dict)
            return 0
        else:
            dealer.add_to_count(card_count_dict)
            player.add_to_count(card_count_dict)
            return -1
        

    if player.natural():
        player.add_money(round(bet_amount * 1.25) + bet_amount)
        player.add_to_count(card_count_dict)
        if dealer.peek().rank in card_count_dict.keys():
            card_count_dict[dealer.peek().rank] += 1
        else:
            card_count_dict[dealer.peek().rank] = 1

        return 1


    # player goes through process
    player_continue_flag = True
    split_flag = False

    while (player_continue_flag):
        if BASIC_STRATEGY:
            result = basic_strategy(player,dealer)
        else:
            result = dealer_strategy(player)


        # for now just going to leave all of the doubles as hit
        if (result.name == "STAND"):
            player_continue_flag = False

        if (result.name == "DOUBLE"):
            if player.money >= bet_amount:
                player.bet(bet_amount)
                bet_amount *= 2
                player.add_card(deck.pop())
                player_continue_flag = False
            else:
                player.add_card(deck.pop())

        if (result.name == "SPLIT"):
            if player.money >= bet_amount:
                split_flag = True
                player_split_1 = Player()
                player_split_2 = Player()
                
                player.bet(bet_amount)

                player_split_1.add_card(player.hand.pop())
                player_split_2.add_card(player.hand.pop())


                for i in [player_split_1, player_split_2]:
                    i.add_card(deck.pop())
                    player_split_continue_flag = True
                    while (player_split_continue_flag):
                        result = basic_strategy(i, dealer)

                        if (result.name == "STAND"):
                            player_split_continue_flag = False

                        else:
                            i.add_card(deck.pop())
                            if (i.bust() or i.get_hand_value() == 21):
                                player_split_continue_flag = False

            else:
                player.add_card(deck.pop())


        if (result.name == "HIT" or result.name == "SPLIT"):
            player.add_card(deck.pop())
            if player.bust():
                return -1
            if (player.get_hand_value() == 21):
                player_continue_flag = False

    # dealer goes through process
    dealer_continue_flag = True
    while (dealer_continue_flag):
        result = dealer_strategy(dealer)

        if (result.name == "STAND"):
            dealer_continue_flag = False

        if (result.name == "HIT"):
            dealer.add_card(deck.pop())
            if dealer.bust():
                player.add_money(2 * bet_amount)
                return 1
            if (dealer.get_hand_value() == 21):
                dealer_continue_flag = False

    dealer.add_to_count(card_count_dict)
    player.add_to_count(card_count_dict)

    # compare hands
    if split_flag:
        wins = []

        for i in [player_split_1, player_split_2]:
            print(f"current hand({i.get_hand_value()}): {i.hand}")
            if dealer.get_hand_value() > i.get_hand_value() or i.get_hand_value() > 21:
                wins.append(-1)
            elif dealer.get_hand_value() == i.get_hand_value():
                player.add_money(bet_amount)
                wins.append(0)
            elif dealer.get_hand_value() < i.get_hand_value():
                player.add_money(bet_amount * 2)
                wins.append(1)
        print(f"dealer hand({dealer.get_hand_value()}): {dealer.hand}\n\n")

        if sum(wins) == 0:
            return 0
        if sum(wins) > 0:
            return 1
        if sum(wins) < 0:
            return -1

    else:
        if dealer.get_hand_value() > player.get_hand_value():
            return -1
        if dealer.get_hand_value() == player.get_hand_value():
            player.add_money(bet_amount)
            return 0
        if dealer.get_hand_value() < player.get_hand_value():
            player.add_money(bet_amount * 2)
            return 1


if __name__ == "__main__":
    number_of_experiments = 1000

    money_results = []
    for i in range(number_of_experiments):
        ending_money = main()
        money_results.append(ending_money)

    array = np.array(money_results)
    df = pd.DataFrame(array)
    print(df.describe())
