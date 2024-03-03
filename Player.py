from collections import namedtuple

Card = namedtuple('Card', ['suit', 'rank'])


class Player:

    def __init__(self, initial_money: int = 1000):
        self.money = initial_money
        self.hand = []

    def add_card(self, card: Card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def get_hand_value(self) -> int:
        total = 0
        for i in self.hand:
            if i.rank not in list("AKQJ"):
                total += int(i.rank)
            if i.rank in list("KQJ"):
                total += 10
            if i.rank == "A":
                if (total + 11 > 21):
                    total += 1
                else:
                    total += 11

        return total

    def peek(self) -> Card:
        return self.hand[0]

    def bust(self) -> bool:
        """
        returns true if busted. false otherwise
        """
        if self.get_hand_value() > 21:
            return True

        return False

    def natural(self) -> bool:
        """
        returns true if has natural. false otherwise
        """
        if (self.get_hand_value() == 21 and len(self.hand)):
            return True
        return False

    def add_money(self, amount: int):
        self.money += amount

    def bet(self, amount: int) -> int:
        amount = min(amount, self.money)
        self.money -= amount

        return amount

    def get_ace_positions(self) -> list:
        result = []
        for index, card in enumerate(self.hand):
            if card.rank == "A":
                result.append(index)

        return result
    
    def add_to_count(self, card_count_dict: dict):
        for i in self.hand:
            if i.rank in card_count_dict.keys():
                card_count_dict[i.rank] += 1
            else:
                card_count_dict[i.rank] = 1
