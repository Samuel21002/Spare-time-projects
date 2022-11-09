from __future__ import annotations
from dataclasses import dataclass, replace
from getkey import key
from sys import stdout
from time import sleep
import random
import re

##
# Game of Poker
##

"""- gameRunning is True until user presses 'q' upon prompt.
   - Regex for user input is set to digits separated by comma, whitespace optional"""
gameRunning = True
choice_re = re.compile(r"^\s*?[0-5]\s*?(,\s*?[1-5]\s*?){0,4}\s*?$")


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ValueTooSmallOrBig(Error):
    """Raised when the input value is not between 1 and 5"""
    pass


# Card instance class
@dataclass
class Card():

    suit: str
    value: int

    __slots__ = ["suit", "value"]

    def __str__(self):
        return self.suit + str(self.value)


#Deck consisting of 52 cards
class Deck():

    cards = []

    def allCards(self):
        print(f"Length of the deck: {len(deck.cards)}")
        for i in deck.cards:
            print(i.suit + str(i.value))

    def __init__(self):

        for i in range(1, 14):

            self.cards.append(Card("H", i))
            self.cards.append(Card("C", i))
            self.cards.append(Card("S", i))
            self.cards.append(Card("D", i))

# Create a deck instance and the dealer list consisting of 5 cards 
deck = Deck()
dealer = []


def checkDealer():

    if (len(dealer) > 5):
        print("Too many cards")

    elif (len(dealer) < 5):
        print("Too few cards")


def drawFromDeck() -> Card:
    """ Draws a random card from the deck """

    card = deck.cards.pop(random.randint(0, len(deck.cards) - 1))
    
    try:
        return card

    except IndexError:
        print("ERROR! List out of index! Drawing a new card")
        

# Displays all dealer cards


def showCards(dealer):
    """Displays the cards"""

    try:
        stdout.write("\n*********************************")
        stdout.write("\n")
        for i in dealer:
            stdout.write(f"*[{i.__str__()}]*")
            stdout.flush()
            sleep(0.1)
        stdout.write("\n")
        stdout.write("*********************************\n\n")
    except:
        stdout.write("Cannot find cards!")


# Winning hand flashy text
def flashyText(text: str) -> None:

    """Displays a message in a 'popup box' """
    stdout.write("\n--------------------------------")
    stdout.write("\n")
    stdout.write(text)
    stdout.flush()
    sleep(0.4)
    stdout.write("\n")
    stdout.write("--------------------------------\n")
    stdout.write("\n")


def checkForWin():

    """ All final dealers cards, both suits and values, are registered into 2 dicts """

    # Variables keeping count of number of pairs and three of a kind
    pair_amt = 0
    three_of_kind = 0

    # The count of different suits and cards
    suit_amounts = {
        "Clubs": sum(x.suit == 'C' for x in dealer),
        "Spades": sum(x.suit == 'S' for x in dealer),
        "Diamonds": sum(x.suit == 'D' for x in dealer),
        "Hearts": sum(x.suit == 'H' for x in dealer),
    }

    value_amounts = {

        "Ones": sum(x.value == 1 for x in dealer),
        "Twos": sum(x.value == 2 for x in dealer),
        "Threes": sum(x.value == 3 for x in dealer),
        "Fours": sum(x.value == 4 for x in dealer),
        "Fives": sum(x.value == 5 for x in dealer),
        "Sixes": sum(x.value == 6 for x in dealer),
        "Sevens": sum(x.value == 7 for x in dealer),
        "Eights": sum(x.value == 8 for x in dealer),
        "Nines": sum(x.value == 9 for x in dealer),
        "Tens": sum(x.value == 10 for x in dealer),
        "Jacks": sum(x.value == 11 for x in dealer),
        "Queens": sum(x.value == 12 for x in dealer),
        "Kings": sum(x.value == 13 for x in dealer)

    }

    """ For loop checks if the user has a winning hand based on dict values. If the amount of the same values exceeds 1 then it is
    either a pair, three of a kind or four of a kind """
    for card_count in value_amounts.values():

        # Amount of Pairs
        if card_count > 1:
            pair_amt += 1

        # Three Of Kind
        if card_count == 3:
            three_of_kind += 1

        # Four of kind
        elif card_count == 4:
            flashyText("You got four of kind!")
            break

        #Note! Five of kind with joker? Update later!

    """ If amount of pairs = 2 then its two pairs or possibly full house. 
        If it's three of kind, it can't be two pair but if it's both, its full house """

    if pair_amt == 2 and three_of_kind == 0:
        flashyText("You got two pairs!")

    elif three_of_kind == 1:
        flashyText("You got three of a kind!")

    elif pair_amt == 1 and three_of_kind == 1:
        flashyText("You got a full house!")

    else:
        """ Else, check for straight, flush or straight flush """

        """ A Straight hand : Find the lowest value (x) by iterating through the dealers cards. Then from a range from 
        x to x+5, check if the 'value_amounts' -variable has such values for each iteration from x to x+5.

        A flush : Check if the 'suit_amounts' has 5 cards aka. all cards belong to one suit """

        straight_count = 0

        for x in range(min(value_amounts.values()), min(value_amounts.values()) + 5):
            if x in value_amounts.values():
                straight_count += 1

        flush = False
        for s in suit_amounts.values():
            if s == 5:
                flush = True
                break

        if straight_count == 5 and flush == False:
            flashyText("You got a straight!")

        elif straight_count == 5 and flush == True:
            flashyText("You got a straight flush!")

        elif straight_count < 5 and flush == True:
            flashyText("You got a flush!")

    print("SUITS:\n", suit_amounts)
    print("VALUES:\n", value_amounts)

    suit_amounts.clear()
    value_amounts.clear()


#################               #################
#################   THE GAME    #################
#################               #################


print("Welcome to Poker!\n")
print("Type anything to start. Type 'q' to quit")
prompt = input()

# If user prompt is "y", game starts
if (prompt != "q".casefold() or prompt == key.ENTER):

    while (gameRunning):

        # Draw 5 random cards
        dealer = []
        dealer.extend([drawFromDeck() for i in range(5)])
        checkDealer()  # Just for checking the number of list appends
        showCards(dealer)  # Displays the cards

        """While 'userchoice' is not an integer or within the proper range, program throws an exception"""
        while True:

            try:
                userchoice = input(
                    "Pick your cards to swap [1-5], or choose '0' to skip: ")

                if not bool(re.match(choice_re, userchoice)):
                    print("Wrong input!")
                    continue

                elif userchoice == 0:
                    break

                else:
                    choice_list = set(map(int, [x.replace(" ", "")
                    for x in re.match(choice_re, userchoice).group().split(",")]))
                    break

            except ValueError:
                if userchoice == key.ENTER:
                    userchoice = None
                    break

                print("Something went wrong")
                continue

        """Change the cards depending on the amount of cards swapped. If no cards were selected, nothing happens"""
        for d in range(1, 6):
            if d in choice_list:
                dealer[d-1] = drawFromDeck()

        # Displays the cards in the console
        showCards(dealer)

        # A message is displayed if the dealer has a winning hand 
        checkForWin()

        # If user wants to play again, re-initialize the deck. If not, the game stops
        print("Wanna play again? Type anything. Type 'q' to quit")
        prompt = input()

        if (prompt == "q".casefold() or prompt == key.ENTER):

            gameRunning = False
            print("Thank you for playing!")

        deck.cards.clear()
        deck.__init__()

# If user doesn't press 'y' the game stops
else:
    print("The game has exited, thank you for playing!")
    gameRunning = False
