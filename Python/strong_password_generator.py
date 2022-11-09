from __future__ import annotations
from statistics import mean
from enum import Enum
from collections import Counter
from string import punctuation as specialchars
import random as rnd
import re
import sys

"""
What Makes a Password Strong? 
The key aspects of a strong password are length (the longer the better); 
a mix of letters (upper and lower case), numbers, and symbols, 
no ties to your personal information and no dictionary words.
Password Length
Allow Symbols (!@#$%^&*()+)
Allow Numbers (0-9)Allow Lowercase (abc)
Allow Uppercase (ABC)Exclude Duplicate Characters
Exclude Similar (iI1loO0)Allow Other Symbols (~`[];?,)"""


try:
    pw_length: str = 0
    pw_mixcase: bool = True
    pw_symbols: bool = True
    pw_familiar: str

    # The equivalents to different alphabetical characters
    leet_chars = ("Aa4", "Bb6", "Cc", "Dd", "Ee3", "Ff", "Gg9", "Hh", "Ii1", "Jj", "Kk", "Ll", "Mm", "Nn",
                    "Oo0", "Pp", "Qq", "Rr", "Ss5", "Tt", "Uu", "Vv7", "Ww", "Xx", "Yy", "Zz", " ")

    sysargs = str(sys.argv[1])

    class Strength(Enum):

        WEAK = 1
        MEDIUM = 2
        STRONG = 3
        SUPERB = 4

    def check_pw_length(length: str) -> Strength:
        """Checks the password length and returns a proper Enum value"""

        match len(length):
            case num if num in range(1, 6):
                return Strength.WEAK
            case num if num in range(6, 13):
                return Strength.MEDIUM
            case num if num in range(13, 16):
                return Strength.STRONG
            case num if num > 16:
                return Strength.SUPERB
            case _:
                return Strength.WEAK

    def randomness(word: str) -> Strength:
        """Measures occurrences of a char in string, the less prevalent from the average the better"""

        rating: int = 0

        if word:

            x = Counter([w for w in word])
            letter_cnt_avg = round(mean(x.values()))
            print(f"Character {x}")

            for v in x.values():
                if not v > letter_cnt_avg:
                    rating += 1

            match (rating):
                case num if num < 3 and len(word) < 6:
                    return Strength.WEAK
                case num if num in range(3, 8) and len(word) < 6:
                    return Strength.WEAK
                case num if num < 3 and len(word) > 6:
                    return Strength.MEDIUM
                case num if num in range(3, 8):
                    return Strength.MEDIUM
                case num if num > 8:
                    return Strength.STRONG
                case num if num > 8 and len(word) >16:
                    return Strength.SUPERB
                case _:
                    return "You string is empty"

        # Note! Add feature for checking to see whether they are the letters in alphabetical order or numbers in order
        # Note! Add feature for checking if every other char is digit, special character or letter

    def leet_stringify(word: str) -> str:
        """ Iterates through the string, replaces each char with a random letter from the list of leet-letters """

        leetword = []

        if word:

            for char in word:
                for c in leet_chars:
                    if char in c and not char.isdigit():
                        leetword.append(c[rnd.randint(0, len(c) - 1)])
                    elif char.isdigit():
                        leetword.append(char)
                        break

            leetword_no_space = re.sub(" ", specialchars[rnd.randint(0, len(specialchars))], ''.join(leetword))  # Replaces spacebars with a random special character

            return leetword_no_space

        return "Your string is empty"

    def run_pw_check(word: str) -> str:
        """ Runs a thorough testing of a password using all the functions provided above """

        try:
            leetword = leet_stringify(word)
            print("\nThe leet version of the word is: ", leetword)
            print("The randomness index of the password is: ",
                  randomness(leetword).name)
            print("The password length index if the word is: ",
                  check_pw_length(word).name)
            return "\nPw-check succesful!"
            
        except:
            print("Sorry! Something went wrong, run the program again!")

    #Run the password check by providing system args in console
    print(run_pw_check(sysargs))

except:
    print("Error! Provide one string value to generate the password!")
