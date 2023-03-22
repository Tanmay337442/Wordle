import random


# set global constants
NUMGUESSES = 6
NUMLETTERS = 5

# function to get and delete first item from sequence
def new(sequence):
    chosen = sequence[0]
    del sequence[0]
    return chosen

# compare guess and answer
def test(guess, answer):
    word2 = list(answer)
    result = []
    for x in range(len(guess)):
        # find correct letters
        if guess[x] == word2[x]:
            result.append("correct")
            word2[x] = 0
        # find present letters
        elif guess[x] in word2:
            result.append("present")
            word2[word2.index(guess[x])] = 0
        # all other letters are absent
        else:
            result.append("absent")   
    # return 5 item list containing result for each letter
    return result

# add letter to guess
def add_letter(key, guess):
    guess.append(key.upper())
    return guess

# delete letter from guess
def delete(guess):
    del guess[-1]
    return guess

# check for win
def win(sequence):
    # 5 letters are all correct
    if sequence == ["correct" for x in range(NUMLETTERS)]:
        return True

# check for loss
def loss(sequence, answer):
    # no more guesses and last guess is not correct
    if len(sequence) == NUMGUESSES and answer != "".join(sequence[-1]):
        return True
    return False

# check for valid word
def valid(guess, valid):
    # correct number of letters
    if len(guess) == NUMLETTERS:
        # word in list of valid words
        if "".join(guess) in valid:
            return True
    return False

