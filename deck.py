"""
deck.py
Author: William Ughetta
Implements a standard 52 deck of playing cards and Knuth Shuffle.
"""

from enum import Enum
from random import randint

class Deck:
    """
    Implements a deck from which one card can be selected at a time.
    Deck is initialized as shuffled and re-shuffling it will restore all
    missing cards.
    """

    # `cards` list holds pointers to the ORDERED_52_CARDS array. The order
    # of the pointers is the order of the deck. The right side is the top.
    cards = []

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        """
        Restores the deck to 52 cards and shuffles the positions.
        """
        self.cards = [index for index in range(N_CARDS)]
        knuth_shuffle(self.cards)

    def pop(self):
        """
        Pop the card on top of the deck (right-most in the array)
        """
        return ORDERED_52_CARDS[self.cards.pop()] if (len(self.cards) > 0) else None

    def __iter__(self):
        """ Implement the iterator protocol """
        return self

    def __next__(self):
        """ Implement the iterator protocol """
        if len(self.cards) <= 0:
            raise StopIteration
        else:
            return self.pop()

def knuth_shuffle(array):
    """
    Randomly shuffles an array in linear time using Knuth's algorithm.
    Algorithm: Traverse array and randomly pick the current index or one
    to the left of it. Then swap the current index and the random one.
    Method from Princeton COS 226 Algorithms and Data Structures.
    """
    for i in range(len(array)):
        random = randint(0, i)
        swp = array[random]
        array[random] = array[i]
        array[i] = swp

class Card:
    """ Represents one card for example the Two of Hearts """
    def __init__(self, value, suite):
        assert value >= 1 and value <= N_VALUES
        assert isinstance(suite, Suites)
        self.value = value
        self.suite = suite.value

    def value_to_string(self):
        """ Convert value to a string """
        return VALUES_TO_NAMES[self.value]

    def is_face_card(self):
        """ A Face card is a Ace, Jack, Queen, or King """
        return (self.value is 1 or self.value > 10)

    def is_ace(self):
        """ Check if is the Ace """
        return (self.value is 1)

    def get_short_name(self):
        """ Return a string representation with abbreviated suite """
        return self.value_to_string() + " of " + self.suite['symbol']

    def __repr__(self):
        """ Print representation """
        return self.value_to_string() + " of " + self.suite['name']

    def __eq__(self, other):
        """ Equality """
        return (self.value == other.value) and (self.suite == other.suite)

class Suites(Enum):
    """ There are four playing card suites. """
    clubs = {'name':'Clubs', 'symbol':'♣', 'color':'black'}
    diamonds = {'name':'Diamonds', 'symbol':'♦', 'color':'red'}
    spades = {'name':'Spades', 'symbol':'♠', 'color':'black'}
    hearts = {'name':'Hearts', 'symbol':'♥', 'color':'red'}

# Deck constants
N_CARDS = 52
N_SUITES = 4
N_VALUES = 13

# Constant of all 52 cards in a standard playing deck.
ORDERED_52_CARDS = [Card(value+1, suite) for suite in Suites for value in range(N_VALUES)]

# Lookup dictionary for converting card values to names
VALUES_TO_NAMES = {
    1: "Ace",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Jack",
    12: "Queen",
    13: "King",
}
