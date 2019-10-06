"""
test.py
Author: William Ughetta
Tests for the BlackJack game
"""

# Test suite imports
from unittest import TestCase
from unittest import main

# BlackJack imports
from blackjack import Game
from deck import Deck
from deck import Card
from deck import Suites
from deck import N_CARDS
from deck import knuth_shuffle
from player import Player

class TestPlayer(TestCase):
    """
    Unit tests players by checking their hands and the counts they produce.
    """

    def test_hand_count(self):
        """
        Check that hand counts are accurately summed up using all of the special
        rules, which are face cards are worth 10. Aces are worth 1 or 11, and other
        cards are worth their normal value (i.e. 6 is worth 6).
        """

        # Test empty hand
        bob = Player('B.O.B.', is_computer=False)
        self.assertTrue(len(bob.hand) == 0)
        self.assertTrue(bob.get_hand_count() == 0)

        # Test Ace, Jack == 21
        bob.hand = [Card(1, Suites.diamonds), Card(11, Suites.spades)]
        self.assertTrue(bob.get_hand_count() == 21)

        # Test Ace, Jack, Queen == 21
        bob.hand = [Card(1, Suites.diamonds), Card(11, Suites.spades), Card(12, Suites.clubs)]
        self.assertTrue(bob.get_hand_count() == 21)

        # Test Ace, Ace, Ace, Ace, Jack, Seven == 21
        bob.hand = [Card(1, Suites.clubs), Card(1, Suites.diamonds), Card(1, Suites.hearts),
                    Card(1, Suites.spades), Card(11, Suites.spades), Card(7, Suites.clubs)]
        self.assertTrue(bob.get_hand_count() == 21)

        # Test hand with only one of each card
        for card in Deck():
            bob.hand = [card]
            if card.value is 1:
                # Ace is worth 11 when below 21
                self.assertTrue(bob.get_hand_count() == 11)
            elif card.value < 11:
                self.assertTrue(bob.get_hand_count() == card.value)
            else:
                # Face cards (jack, queen, king) worth 10
                self.assertTrue(bob.get_hand_count() == 10)

        # Test every possible combination of two card hand counts
        for first in Deck():
            for second in Deck():
                count = 0
                # Add first card with aces counting 1
                if first.value > 10:
                    count += 10
                else:
                    count += first.value
                # Add second card with aces counting 1
                if second.value > 10:
                    count += 10
                else:
                    count += second.value
                # Add first ace as 11 if won't go over 21
                if (first.value == 1) and (count + 10 <= 21):
                    count += 10
                # Add second ace as 11 if won't go over 21
                if (second.value == 1) and (count + 10 <= 21):
                    count += 10

                # Make sure get_hand_count is equal
                bob.hand = [first, second]
                self.assertTrue(bob.get_hand_count() == count)

    def test_over_21(self):
        """
        Verifies player's hand accuratley is_over_21 only when the card count is over 21.
        """

        # Our star player
        bob = Player('B.O.B.', is_computer=False)

        # Hand count 0
        self.assertTrue(bob.get_hand_count() == 0)
        self.assertFalse(bob.is_over_21())

        # Hand count 21
        bob.hand = [Card(1, Suites.diamonds), Card(11, Suites.spades)]
        self.assertTrue(bob.get_hand_count() == 21)
        self.assertFalse(bob.is_over_21())

        # Hand count 22
        bob.hand = [Card(11, Suites.diamonds), Card(11, Suites.spades), Card(2, Suites.clubs)]
        self.assertTrue(bob.get_hand_count() == 22)
        self.assertTrue(bob.is_over_21())

        # Hand count 50
        bob.hand = [Card(10, Suites.diamonds), Card(11, Suites.spades), Card(12, Suites.clubs), Card(13, Suites.hearts), Card(11, Suites.clubs)]
        self.assertTrue(bob.get_hand_count() == 50)
        self.assertTrue(bob.is_over_21())

class TestDeck(TestCase):
    """
    Unit and stress tests the Deck by checking for a complete, valid
    deck; attempting to construct illegal cards; and statistically
    testing the knuth shuffling algorithm.
    """

    def test_illegal(self):
        """ Make illegal cards """
        with self.assertRaises(AssertionError):
            Card(0, Suites.clubs)
        with self.assertRaises(AssertionError):
            Card(14, Suites.diamonds)
        with self.assertRaises(AssertionError):
            Card(1, {'FakeSuite', '!', 'orange'})

    def test_complete(self):
        """
        Test the deck is complete. And stress test it.
        """
        # Make all legal cards
        full_deck = []
        for suite in Suites:
            for i in range(1, 14):
                full_deck.append(Card(i, suite))
        self.assertTrue(len(full_deck) == N_CARDS)

        # Check that a deck contains all legal cards only
        deck = Deck()
        visited_deck = []
        for card in deck:
            self.assertTrue(card in full_deck)
            self.assertFalse(card in visited_deck)
            visited_deck.append(card)
        self.assertTrue(len(full_deck) == len(visited_deck))

        # Check that there are no more cards left
        self.assertTrue(deck.pop() is None)
        self.assertTrue(deck.pop() is None)
        self.assertTrue(deck.pop() is None)

        # Stress test
        for _ in range(1000):
            deck.shuffle()
            visited_deck = []
            for _ in range(N_CARDS):
                c = deck.pop()
                self.assertTrue(c in full_deck)
                self.assertFalse(c in visited_deck)
                visited_deck.append(c)
            self.assertTrue(len(visited_deck) == N_CARDS)
            self.assertTrue(deck.pop() is None)

    def test_shuffle(self):
        """
        Stress tests the knuth shuffling algorithm and checks that when
        N_CARD numbers are shuffled they appear in different bins at least
        some fraction of N_TESTS / N_CARDS number of times.
        """
        N_TESTS = 10000

        # results[N_CARDS][N_CARDS] rows are each card (i.e The Ace of Spades) and
        # columns are counts of the number of times the card was shuffled
        # into that index (order) of the deck by the knuth shuffle algo.
        results = [[0 for n in range(N_CARDS)] for m in range(N_CARDS)]

        # Calculate the position of for each card 10000 times
        for _ in range(N_TESTS):
            array = [n for n in range(N_CARDS)]
            knuth_shuffle(array)
            for position in range(N_CARDS):
                results[array[position]][position] += 1

        # The IDEAL_THRESHOLD is closest to the expected statistical outcome
        IDEAL_THRESHOLD = N_TESTS / N_CARDS
        # The accepted thresholds may be about 50% off the ideal one
        # Using a larger N_TESTS would take more time but is expected to be closer to the IDEAL_THRESHOLD
        MAX_ACCEPTED_THRESHOLD = IDEAL_THRESHOLD * 1.50
        MIN_ACCEPTED_THRESHOLD = IDEAL_THRESHOLD * 0.50

        # Verify each card's accumulated positions is within the accepted range
        for card in range(52):
            for position in range(52):
                self.assertTrue(results[card][position] <= MAX_ACCEPTED_THRESHOLD,
                    msg="The value " + str(results[card][position]) +
                        " was above the max statistical threshold of " + str(MAX_ACCEPTED_THRESHOLD))
                self.assertTrue(results[card][position] >= MIN_ACCEPTED_THRESHOLD,
                    msg="The value " + str(results[card][position]) +
                        " was below the min statistical thresh of " + str(MIN_ACCEPTED_THRESHOLD))

if __name__ == '__main__':
    main()
