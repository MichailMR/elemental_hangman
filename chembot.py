import discord
from discord.ext import commands
import json
import random

with open('./rescources/periodic_table.json', 'r', encoding="utf8") as periodic_table:
    elements_dict = json.loads(periodic_table.read())["elements"]
    elements = [{"name":element["name"], "symbol":element["symbol"]} for element in elements_dict]
    
    periodic_table.close()

class chem_game:
    def init(self):
        self.is_playing = False

    async def start(self, ctx, language='nl'):
        await ctx.send('Thinking of a good word...')
        
        with open(f'./elemental_words/elemental_hangman_{language}.json', 'r', encoding="utf8") as input_words:
            word_dict = json.loads(input_words.read())
            word = random.choice(list(word_dict.items()))
            elemental_word = word[1]
            full_word = word[0]
            
            input_words.close()

        stripes = ['⏤' for element in elemental_word]
        total_letters = len(full_word)
        incorrect_symbols = []

        while not stripes == elemental_word and self.is_playing:
            description = f'{total_letters} letter word:\n\n{" ".join(stripes)}\n\n{" ".join(incorrect_symbols)}'
            await ctx.send(embed=discord.Embed(description=description, color=0xaa8800))
                    
            def is_channel(m):
                return m.channel.id == ctx.channel.id
            input_str = (await bot.wait_for("message", check=is_channel)).content
            
            if len(input_str) > 0 and input_str[0] == '?':
                if input_str[1:] in ['a','answer','help','ping']:
                    await ctx.invoke(bot.get_command(input_str[1:]))
                continue
            
            input_symbol = [element["symbol"] for element in elements if element["name"].upper() == input_str.upper()]

            if len(input_symbol) > 2 or len(input_symbol) < 1:
                await ctx.send(f'\n{input_str} is not an elemental name')
                continue
            else:
                input_symbol = input_symbol[0]
            
            guess = input_symbol[0].upper() + (input_symbol[1].lower() if len(input_symbol) > 1 else '')
            
            if not guess in [element["symbol"] for element in elements]:
                await ctx.send(f'\n{input_str} is not an elemental name')
                continue
            
            if guess in elemental_word:
                indices = [i for i, element in enumerate(elemental_word) if element == guess]
                for i in indices:
                    stripes[i] = elemental_word[i]
                
                await ctx.send(f'\n{guess} is in the word')
            else:
                
                if guess[0].lower() in full_word:
                    incorrect_symbol = '__'+guess[0]+'__'
                    if len(guess) > 1:
                        incorrect_symbol = incorrect_symbol[:-2]+guess[1]+'__' if guess[1].lower() in full_word else incorrect_symbol+guess[1]
                else:
                    incorrect_symbol = guess[0]
                    if len(guess) > 1:
                        incorrect_symbol += '__'+guess[1]+'__' if guess[1].lower() in full_word else guess[1]
                
                incorrect_symbols += [incorrect_symbol]
                await ctx.send(f'\n{incorrect_symbol} is not in the word')

        await ctx.send(f'The word was: {" ".join(elemental_word)}')
        
games = []

bot = commands.Bot(command_prefix = '?')

@bot.event
async def on_ready():
    print('Rubiris is ready!')
    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command(help = 'Starts a game', aliases=['s'])
async def start(ctx, *args):
    global games
    channel_id = ctx.channel.id
    
    index = [index for index, game in enumerate(games) if game["id"] == channel_id]
    if len(index) > 0:
        games.pop(index[0])
    
    games += [{"game":chem_game(), "id":ctx.channel.id}]
    game = games[-1]["game"]
    
    game.is_playing = True
    if len(args) > 0 and args[0] in ['nl', 'eng']:
        await game.start(ctx, language=args[0])
    else:
        await game.start(ctx)
    
@bot.command(help = 'Ends the game and reveals the answer', aliases=['a'])
async def answer(ctx, *args):
    channel_id = ctx.channel.id
    
    index = [index for index, game in enumerate(games) if game["id"] == channel_id]
    if len(index) > 0:
        games[index[0]]["game"].is_playing = False


token = json.load(open('../key.json'))["token"]
bot.run(token)