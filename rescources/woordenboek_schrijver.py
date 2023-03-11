import json

with open('./woordenboek.txt', 'r', encoding="utf8") as woordenboek, open('./woordenboek.json', 'w', encoding="utf8") as woordenboek_dict:
    woordenlijst = woordenboek.read().split('\n')
    dict = dict(zip(woordenlijst, ['' for woord in woordenlijst]))
    
    woordenboek_dict.write(json.dumps(dict))
    
    woordenboek.close()
    woordenboek_dict.close()