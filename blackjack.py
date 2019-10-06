"""
blackjack.py
Author: William Ughetta
A Blackjack command line interface frontend
"""

import time

# Blackjack imports
from game import Game

def main():
    """
    Runs a game of blackjack.
    """

    print("Welcome to BlackJack!!!")

    # Ask for number of players
    n_players = get_num_players()

    # Initialize the game
    human_name = 'You'
    game = Game(n_players, human_name=human_name)

    while (True):
        # Deal
        print_deal(game.deal())

        # Play one turn per player
        while game.can_play():
            play_turn(game)
            game.next_player()

        # Output results
        print_score(game, *game.get_winners())
        if (input("Play again? [Y/n] ") is 'n'):
            break

    # End the game
    print("Thanks for playing! Have a great day!")

def get_num_players():
    """
    Return the number of players
    """
    n_players = int(input("Enter number of computer players (0 to 10): "))
    if n_players < 0 or n_players > Game.MAX_COMPUTER_PLAYERS:
        n_players = Game.MAX_COMPUTER_PLAYERS
    print("Okay, playing with the dealer, you, and " + str(n_players) +
            " other computer player(s).")
    time.sleep(0.5)
    return n_players

def print_deal(players):
    """
    Make the dealing process exciting by waiting
    """
    print("Shuffling Cards...")
    time.sleep(1)
    print("Dealing...")
    time.sleep(1)
    for player in players:
        print(player)
        time.sleep(0.5)
    print("Finished Dealing.")
    time.sleep(0.5)

def play_turn(game):
    """
    Play one turn by either outputting computer moves or inputting human moves
    """
    print('=================================')
    if game.is_current_player_a_computer():
        print(game.get_current_player_name() + "'s turn to play")
        time.sleep(0.5)
        cards_drawn = game.play_computer_turn()
        for card in cards_drawn:
            if card is not None:
                print("Hit! Drew card %s" % card)
                time.sleep(0.5)
            else:
                print("Deck is empty! Finished turn.")
        if (game.current_player.is_over_21()):
            print(game.get_current_player_name() + " lost! " + game.get_current_player_name() + " is out.")
            time.sleep(0.5)
        else:
            if game.get_current_player_name != 'Dealer':
                print(game.get_current_player_name() + " finished with count of " + str(game.get_current_player_hand_count()))
            time.sleep(0.5)
    else:
        print("Your turn to play! Your count is: %s" % game.get_current_player_hand_count())
        print("Your hand is: %s" % game.get_current_player_hand())
        while game.human_can_draw() and input("Do you want to hit? [y/N] ") is 'y':
            card = game.human_player_draw()
            if card is not None:
                print("Hit! Delt card %s. Your count is now: %s" % (card, game.get_current_player_hand_count()))
                print("Your hand is: %s" % game.get_current_player_hand())
            else:
                print("Deck is empty! Finished turn.")
                break
        if game.is_current_player_over_21():
            print("You lost! You score is over %s." % game.max_count())


def print_score(game, dealer_count, winners, human_name='You'):
    """
    Prints out a summary of who won and if the player lost
    """

    # Print winners and scores
    print("Dealer had a count of %s" % dealer_count)
    if dealer_count > game.max_count():
        print("Dealer lost! Winners:")
    print("\n".join([str(name) + " won with a count of %s" % score for (name, score) in winners]))
    
    # Print if Human won or lost
    winner_names = [name for (name, score) in winners]
    if human_name in winner_names:
        winner_scores = [score for (name, score) in winners]
        human_score = winner_scores[winner_names.index(human_name)]
        print('Congratulations!!! You won with a count of %s' % human_score)
    else:
        print('You lost')

# Start game
if __name__ == '__main__':
    main()