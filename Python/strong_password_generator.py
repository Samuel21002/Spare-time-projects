from __future__ import annotations
from statistics import  mean
from enum import Enum
from collections import Counter
from string import punctuation as specialchars
import random as rnd
import re

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

pw_length : str = 0
pw_mixcase : bool = True
pw_symbols : bool = True
pw_familiar : str

leet_strings = ("Aa4", "Bb6", "Cc", "Dd", "Ee3", "Ff", "Gg9", "Hh", "Ii1", "Jj", "Kk", "Ll", "Mm", "Nn",\
                "Oo0", "Pp", "Qq", "Rr", "Ss5", "Tt", "Uu", "Vv7", "Ww", "Xx", "Yy", "Zz", " ")

class Strength(Enum):

    WEAK = 1
    MEDIUM = 2
    STRONG = 3
    VERY_STRONG = 4

def check_pw_length(length: str) -> Strength:

    """Checks the password length and returns an Enum value"""
    match len(length):
        case num if num in range(1, 6):
            return Strength.WEAK
        case num if num in range(6, 11):
            return Strength.MEDIUM
        case num if num in range(11, 16):
            return Strength.STRONG
        case num if num > 16:
            return Strength.VERY_STRONG
        case _:
            return Strength.WEAK

def randomness(word : str) -> str:

    """Measure occurence of a string, the less prevalent from the average the better"""
    #TAKE COUNTER LENGTH INTO ACCOUNT!!

    rating : int = 0

    if word:

        x = Counter([x for x in word])
        letter_cnt_avg = round(mean(x.values()))
        
        for v in x.values():
            if not v > letter_cnt_avg:
                rating += 1
        
        if rating < 5: return "Weak"
        elif rating in range(5,11): return "Ok"
        elif rating > 10: return "Strong"

    #one for checking to see whether they are the letters in alphabetical order or numbers in order

    #one for checking if every other char is digit, special character or letter

    return "You string is empty"

def leet_stringify(word : str) -> str:
    """Iterate through the string, replace with random letter out of the list of leet letters"""
    leetword = []

    if word:

        for char in word:
            for c in leet_strings:
                if char in c and not char.isdigit():
                    leetword.append(c[rnd.randint(0, len(c) - 1)])
                elif char.isdigit():
                    leetword.append(char)
                    break
                #Why loop?
                # elif char not in c:
                #     leetword.append("moi")

        leetword_no_space = re.sub(" ", specialchars[rnd.randint(0, len(specialchars))], ''.join(leetword))  # Remove spacebars with a random special character

        return leetword_no_space

    return "Your string is empty"


def run_pw_check(word: str) -> None:
    """Do a thorough testing of a password using all the functions above"""
    print("The leet version of the word is: ", leet_stringify(word))
    print("The randomness index of the password is: ", randomness(word))
    print("The password length index if the word is: ", check_pw_length(word))

#print(leet_stringify("Viva La Fiesta"))
print(run_pw_check("abcdefg"))
