import json
import random

with open('./rescources/periodic_table.json', 'r', encoding="utf8") as periodic_table:
    elements_dict = json.loads(periodic_table.read())["elements"]
    elements = [{"name":element["name"], "symbol":element["symbol"]} for element in elements_dict]
    
    periodic_table.close()

with open('./elemental_words/elemental_hangman_nl.json', 'r', encoding="utf8") as input_words:
    word_dict = json.loads(input_words.read())
    word = random.choice(list(word_dict.items()))
    elemental_word = word[1]
    full_word = word[0]
    
    input_words.close()

stripes = ['_' for element in elemental_word]

while not stripes == elemental_word:
    input_str = input('\n'+' '.join(stripes)+'\nInput: ')
    
    input_symbol = [element["symbol"] for element in elements if element["name"].upper() == input_str.upper()]

    if len(input_symbol) > 2 or len(input_symbol) < 1:
        print(f'\n{input_str} is not an elemental name')
        continue
    else:
        input_symbol = input_symbol[0]
    
    guess = input_symbol[0].upper() + (input_symbol[1].lower() if len(input_symbol) > 1 else '')
    
    if not guess in [element["symbol"] for element in elements]:
        print(f'\n{input_str} is not an elemental name')
        continue
    
    if guess in elemental_word:
        indices = [i for i, element in enumerate(elemental_word) if element == guess]
        for i in indices:
            stripes[i] = elemental_word[i]
        
        print(f'\n{guess} is in the word')
    else:
        response = (f'\nThough {guess[0].lower()} is' if guess[0].lower() in full_word else '') + (f'\nThough {guess[1]} is' if len(guess) > 1 and guess[1].lower() in full_word else '')
        print(f'\n{guess} is not in the word', response)

print(f'The word was: {full_word}')