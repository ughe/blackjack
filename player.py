"""
blackjack.py
Author: William Ughetta
Implements Blackjack player scoring logic
"""

class Player:
    """
    Manages one blackjack player (either computer or human) as well as the
    display logic. Hides computers' first cards while showing all human cards.
    """

    # Greatest legal score in BlackJack
    MAX_COUNT = 21

    def __init__(self, name, is_computer=True):
        self.name = name
        self.is_computer = is_computer
        self.hand = []

    def get_hand_count(self):
        """
        Calculates the value of the current hand based on the blackjack
        rules.
        """
        count = 0
        n_aces = 0
        for card in self.hand:
            if card.is_ace():
                count += 11             # ace worth 11 or 1
                n_aces += 1
            elif card.is_face_card():
                count += 10             # non-ace face cards worth 10
            else:
                count += card.value     # non-face cards worth their value

        while (n_aces > 0) and (count > self.MAX_COUNT):
            count -= 10                 # make ace worth 1 instead of 11
            n_aces -= 1

        return count

    def is_over_21(self):
        """
        Checks if player has a count over 21.
        """
        return self.get_hand_count() > 21

    def should_computer_play(self):
        """
        Automated rule for if computer should get another card or not.
        Checks if player has less than 17 points.
        """
        return self.get_hand_count() < 17

    def __repr__(self):
        """
        Show non-computer player hands and  the computer's hand.
        Assumes 1 human player per game.hide
        """
        if self.is_computer:
            if len(self.hand) is 0:
                return self.name + "'s hand is empty."
            else:
                tmp = ["Card Hidden"] + [card.__repr__() for card in self.hand][1:]
                return self.name + " has cards " + str(tmp)
        else:
            if len(self.hand) is 0:
                return "Your hand is empty."
            else:
                return "You have cards " + str(self.hand)
