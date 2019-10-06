"""
game.py
Author: William Ughetta
Backend model for a Blackjack game. Separates business logic from frontend
"""

from random import randint

from deck import Deck
from player import Player

class Game:
    """
    Allows for playing multiple full Blackjack games.
    """

    # Blackjack Constants
    MAX_COMPUTER_PLAYERS = 10
    COMPUTER_NAMES = [
        'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo',
        'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett'
    ]

    def __init__(self, n_players, human_name='You'):
        """
        Initializes all players. Takes number of players excluding the
        Dealer and the Human
        """

        # Set number of players
        if (n_players < 0 or n_players > self.MAX_COMPUTER_PLAYERS):
            self.n_players = self.MAX_COMPUTER_PLAYERS
        else:
            self.n_players = n_players

        self.deck = Deck()

        # Initialize number of players
        self.players = [Player(human_name, is_computer=False),]
        for i in range(self.n_players):
            self.players.append(Player(self.COMPUTER_NAMES[i]))

        # Insert self into random order with the players
        random = randint(0, self.n_players)
        tmp = self.players[0]
        self.players[0] = self.players[random]
        self.players[random] = tmp

        # Add the dealer at the end
        self.players.append(Player('Dealer'))

    def deal(self):
        """
        Shuffles and deals a new deck to the players in the game
        """

        # Shuffle
        self.deck.shuffle()

        # Deal
        for player in self.players:
            player.hand = [self.deck.pop(), self.deck.pop()]
        
        # Set first player
        self.current_player_i = 0
        self.current_player = self.players[0]

        # return list of players with decks as string
        return [str(player) for player in self.players]

    def play_computer_turn(self):
        """
        Play for the computer
        """
        if self.current_player.is_computer:
            acc = []
            while (not self.current_player.is_over_21() and self.current_player.should_computer_play()):
                c = self.deck.pop()
                acc += [c]
                if (c is None):
                    return acc
                self.current_player.hand.append(c)
            return acc
        return []

    def next_player(self):
        """
        Set the turn to the next player or None
        """
        if self.current_player_i + 1 < len(self.players):
            self.current_player = self.players[self.current_player_i + 1]
            self.current_player_i += 1
        else:
            self.current_player = None

    def get_winners(self):
        """
        Returns tuple: (Dealer Score, List of (Winner Name, Winner Score))
        """

        dealer = self.players[-1] # invariant dealer is last player
        dealer_count = dealer.get_hand_count()
        if dealer_count > Player.MAX_COUNT:
            # Everyone who didn't go over 21 wins if the dealer did go over 21
            winners = [(p.name, p.get_hand_count()) for p in self.players[:-1] if not p.is_over_21()]
        else:
            # Only people who did not go over 21 and beat the dealer win if the dealer is under 21
            winners = [(p.name, p.get_hand_count()) for p in self.players[:-1]
                            if not p.is_over_21() and p.get_hand_count() > dealer_count]
        
        return (dealer_count, winners)

    def is_current_player_a_computer(self):
        """ Returns True if current player is not a human """
        if self.current_player is None:
            return None
        return self.current_player.is_computer

    def is_current_player_over_21(self):
        """ Returns True if current player is not a human """
        if self.current_player is None:
            return None
        return self.current_player.is_over_21()

    def get_current_player_name(self):
        """ Returns the currnet player's name """
        if self.current_player is None:
            return None
        return self.current_player.name

    def get_current_player_hand_count(self):
        """ Returns the count of the current player's hand """
        if self.current_player is None:
            return None
        return self.current_player.get_hand_count()

    def get_current_player_hand(self):
        """ Returns the cards in the current player's hand """
        if self.current_player is None:
            return None
        return self.current_player.hand

    def human_can_draw(self):
        """ Determines if current human player can draw card """
        if self.current_player is None:
            return None
        return not self.current_player.is_computer and not self.current_player.is_over_21()

    def human_player_draw(self):
        """ Draws a card for the human player """
        if self.current_player is None:
            return None
        if self.human_can_draw():
            c = self.deck.pop()
            if c is not None:
                self.current_player.hand.append(c)
                return c
        return None

    def can_play(self):
        """ Returns True if someone can play """
        if self.current_player is None:
            return None
        return self.current_player is not None

    def get_next_player(self):
        """ Returns the next player """
        if self.current_player is None:
            return None
        return self.current_player

    def max_count(self):
        return Player.MAX_COUNT