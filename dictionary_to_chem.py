import json

with open('./rescources/woordenboek.json', 'r', encoding="utf8") as dictionary:
    words = list(json.loads(dictionary.read()))
    dictionary.close()

print('Number of words:', len(words))

with open('./rescources/periodic_table.json', 'r', encoding="utf8") as periodic_table:
    elements_dict = json.loads(periodic_table.read())["elements"]
    elements = [{"name":element["name"], "symbol":element["symbol"]} for element in elements_dict]
    periodic_table.close()
    
print('Number of elements:', len(elements))

def double_is_element(element_chars, word):
    split = list(word)[0:2]
    string = ''.join([split[0].upper(), split[1].lower()])
    
    element = next((element for element in elements if element["symbol"] == string), None)
    
    if element == None:
        if len(word[1:]) == 0:
            return None
        else:
            return double_is_element(element_chars, word)
    else:
        if len(word[2:]) == 0:
            return element_chars + [element]
        else:
            return single_is_element(element_chars + [element], word[2:])

def single_is_element(element_chars, word):
    string = word[0].upper()
    
    element = next((element for element in elements if element["symbol"] == string), None)
    
    if element == None:
        if len(word[1:]) == 0:
            return None
        else:
            return double_is_element(element_chars, word)
    else:
        if len(word[1:]) == 0:
            return element_chars + [element]
        else:
            double_string = string+word[1].lower()
            double_element = next((element for element in elements if element["symbol"] == double_string), None)
            if double_element == None:
                return single_is_element(element_chars + [element], word[1:])
            else:
                return double_is_element(element_chars, word), single_is_element(element_chars + [element], word[1:])

with open('./elemental_words/elemental_hangman.txt', 'w', encoding="utf8") as element_words_file:
        #Code needs to be improved for less loss
    element_words = ''
    for word in words:
        try:
            element_chars = single_is_element([], word)
        except:
            continue
        
        if element_chars == None:
            continue
        
        if type(element_chars[0]) == list:
            try:
                for element_chars_i in element_chars:
                    if not element_chars_i == None:
                        element_word = ''
                        for char in element_chars_i:
                            element_word += char["symbol"]+' '
                        
                    element_words += element_word+'\n'
            except:
                type(element_chars[0])
        
        else:
            try:
                element_word = ''
                for char in element_chars:
                    element_word += char["symbol"]+' '
                
                element_words += element_word+'\n'
            except:
                type(element_chars[0])
    
    element_words_file.write(element_words)
    element_words_file.close()
    