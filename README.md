# Blackjack Design Document

## Run the Game

The game works by running the following:

```
python3 blackjack.py
```

And is easy to play by answering `y` or `n` when asked to deal another card.

## Run the Tests

The unit tests account for edge cases and can be run by:

```
python3 test.py
```

The following tests and edge cases are considered:

- Check that the point-value sum of each pair of cards is correct
- Check that fake cards cannot be played and raise the appropriate error
- Check the Knuth Shuffle is statistically random enough after 10,000 shuffles

## Design

The structure is designed modularly. A new frontend could be created by only replacing the `blackjack.py` file. A new card game backend could also be replaced by modifying `game.py` and `player.py`, which contain the rules for the game and the player respectively.

| File           | Description |
| -------------- | ----------- |
| `blackjack.py` | Runs Blackjack. Frontend logic for Command Line Interface |
| `game.py`      | Backend logic for the BlackJack game including deal and turns |
| `player.py`    | Models player's hand and how to count value of cards |
| `deck.py`      | Models a deck of cards and the Knuth Shuffle |
| `test.py`      | Unit tests |


The Deck uses an array of 52 pointers to keep track of cards. These pointers point to a constant array holding the actual Card objects in sorted order. This saves space by not constantly creating new cards.

Decks only have two fundamental operations: pop and shuffle. pop simply removes a card from the deck by removing the last pointer from the list. shuffle first restores all pointers to the list and then uses the Knuth Shuffling algorithm to shuffle the order of the pointers in the array in a uniformly random manner.

The Knuth Shuffling algorithm that is used works by traversing through each element in the array and every time choosing element less than or equal to the current one and swapping the current element with the randomly chosen element.

The unit tests framework use Python's batteries-included library `unittest.TestCase`. Python is generally a very quick and useful scripting language that makes it easy to write modular and pythonic code.
