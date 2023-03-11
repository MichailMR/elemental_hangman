import argparse
import json

parser = argparse.ArgumentParser(description='Transcribes the txt files to json files')
parser.add_argument('input_file', help='Sets the input file')
parser.add_argument('output_file', help='Sets the input file')

args = parser.parse_args()
print(args.input_file, 'to', args.output_file)

with open(args.input_file, 'r', encoding="utf8") as input_file, open(args.output_file, 'w', encoding="utf8") as output_file:
    word_list = input_file.read().split('\n')
    word_dict = dict(zip([word.replace(' ', '').lower() for word in word_list], [word.split(' ')[:-1] for word in word_list]))
    
    output_file.write(json.dumps(word_dict))
    
    input_file.close()
    output_file.close()