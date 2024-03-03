from Player import Player


def winner(dealer: Player, player: Player):
    if (dealer.get_hand_value() == 21 and len(dealer.hand) == 2):
        if (player.get_hand_value() == 21 and len(player.hand == 2)):
            return 0
        else:
            return -1

    if dealer.get_hand_value() > player.get_hand_value():
        return -1
    elif dealer.get_hand_value() == player.get_hand_value():
        return 0
    else:
        return 1

