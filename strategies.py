from Player import Player
from collections import namedtuple
from Choices import choices

def dealer_strategy(player: Player) -> choices:
    if player.get_hand_value() >= 17:
        return choices.STAND
    else:
        return choices.HIT

def basic_strategy(player: Player, dealer: Player)-> choices:

    # first 2 cards
    if len(player.hand) == 2:
        if player.get_hand_value == 21:
            return choices.STAND

        # splitting
        if player.hand[0].rank == player.hand[1].rank:
            #split aces and eights
            if player.hand[0].rank == "8" or player.hand[1].rank == "A":
                return choices.SPLIT
            if player.hand[0].rank == "9":
                if dealer.peek().rank in ["2","3","4","5","6","8","9"]:
                    return choices.SPLIT
            if player.hand[0].rank == "7":
                if dealer.peek().rank in ["2","3","4","5","6","7"]:
                    return choices.SPLIT
            if player.hand[0].rank == "6":
                if dealer.peek().rank in ["2","3","4","5","6"]:
                    return choices.SPLIT
            if player.hand[0].rank == "3" or player.hand[0].rank == 2:
                if dealer.peek().rank in ["4","5","6","7"]:
                    return choices.SPLIT
        # soft total
        if player.hand[0].rank == "A" or player.hand[1].rank == "A":
            if player.hand[0].rank == "9" or player.hand[1].rank == "9":
                return choices.STAND

            if player.hand[0].rank == "8" or player.hand[1].rank == "8":
                return choices.STAND

            if player.hand[0].rank == "7" or player.hand[1].rank == "7":
                if dealer.peek().rank in ["2","3","4","5","6","7","8"]:
                    return choices.STAND
                return choices.HIT
            return choices.HIT

    # hard total
    hard_total = player.get_hand_value()

    if hard_total >= 17:
        return choices.STAND
    if hard_total == 16 or hard_total == 15 or hard_total == 14 or hard_total == 13:
        if dealer.peek().rank in ["2", "3", "4", "5", "6"]:
            return choices.STAND
        return choices.HIT
    if hard_total == 12:
        if dealer.peek().rank in ["4", "5", "6"]:
            return choices.STAND
        return choices.HIT
    if hard_total == 11:
        return choices.DOUBLE
    if hard_total == 10:
        if dealer.peek().rank in ["2","3","4","5","6","7","8","9"]:
            return choices.DOUBLE
        return choices.HIT
    if hard_total == 9:
        if dealer.peek().rank in ["3","4","5","6"]:
            return choices.DOUBLE
        return choices.HIT
    if hard_total < 9:
        return choices.HIT


def card_counting(card_counting_dict: dict):
    TOTAL_CARD_AMOUNT = 52 * 6

    total_card_count = 0

    running_total = 0
    

    for i in card_counting_dict.keys():
        total_card_count += card_counting_dict[i]
        if i in ["2","3","4","5","6"]:
            running_total += card_counting_dict[i]
        if i in ["10", "J", "K", "Q", "A"]:
            running_total -= card_counting_dict[i]

    true_count = round(running_total / round((TOTAL_CARD_AMOUNT - total_card_count) / 52))

    return true_count

