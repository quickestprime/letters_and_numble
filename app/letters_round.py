import string
from random import choices, shuffle
from nltk.corpus import words
import itertools

# nltk.download('words')

# from PyDictionary import PyDictionary
# dictionary=PyDictionary()

all_words = set(words.words())
word_hashmap = dict(zip(all_words, [True for _ in range(len(all_words))]))

all_letters = string.ascii_uppercase
vowels = ['A','E','I','O','U']
consonants = [x for x in all_letters if x not in vowels]

def sample_from_dict(dictionary):
    return choices(list(dictionary.keys()), weights=dictionary.values())[0]

PROB_MASS_FOR_N_VOWELS = {
    1: 0.05,
    2: 0.25,
    3: 0.45,
    4: 0.15,
    5: 0.1
}

def generate_letters():
    n_vowels = sample_from_dict(PROB_MASS_FOR_N_VOWELS)
    game_vowels = choices(vowels, k = n_vowels)
    n_consonants = 9 - n_vowels
    game_consonants = choices(consonants, k = n_consonants)
    all_letters = game_vowels + game_consonants
    shuffle(all_letters)
    return {'game_letters': all_letters}


def generate_combinations(letters):
    generated_words = []
    # Generate permutations of all lengths
    for r in range(1, len(letters) + 1):
        for permutation in itertools.permutations(letters, r):
            word = ''.join(permutation)
            generated_words.append(word)
    generated_words.sort(key=len,reverse=True)
    return generated_words


def solve_game(letters):
    letter_strings = generate_combinations(letters)
    answers = {}
    for string in letter_strings:
        if word_hashmap.get(string.lower()):
            word_length = len(string)
            if word_length not in answers.keys():
                answers[word_length] = [string]
            else:
                answers[word_length].append(string)
    return answers

def process_guess(user_word):
    if word_hashmap.get(user_word.lower()):
            return len(user_word)
    return False


def main():
    game_letters = generate_letters()
    print(f"Today's letters are: {game_letters['game_letters']}")
    player_has_given_valid_word = False
    player_word = input('Enter your word: ')
    
    while not player_has_given_valid_word:
        if word_hashmap.get(player_word.lower()):
            player_has_given_valid_word = True
            player_score = len(player_word)
        else:
            player_word = input(f"Sorry, {player_word} is not an acceptable word. Please enter another word: ")
    
    answers = solve_game(game_letters['game_letters'])
    answer_keys = list(answers.keys())
    best_score = answer_keys[0]
    print(f"Congrats! You found a {player_score} letter word. The best you could do was {best_score}: {set(answers[best_score])}")
    return player_score

if __name__ == '__main__':
    player_score = main()
