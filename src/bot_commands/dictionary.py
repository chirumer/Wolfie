#### imports

import requests
    # for making http requests

from discord import Embed
    # for making embedded messages

from src.bot_commands.generic import too_few_args
    # notify user: command requires more arguments


#### main

#app_id = os.getenv('dictionary_id')
#app_key = os.getenv('dictionary_secret')

def get_definition(word):
        # TEMPORARY 

    definition = None

    try:
        r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}')
        definition = (r.json())[0]['meanings'][0]['definitions'][0]['definition']
    except:
        pass

    return definition

#### exports

    # meta
meta = {
    'name': 'dictionary',
    'aliases': [],
    'description': (
        'find the dictionary definition of a word'
    )
}

    # main command
async def command(ctx):
    action = ctx['action']

    if not action:
        await too_few_args(ctx, 'dictionary', 1)
        return

    message = ctx['message']

    if len(action.split()) > 1:
        await message.reply(
            'too many arguments..\n'
            'this command takes only one argument.\n'
            '**note**: phrases are not supported'
        )
        return

    word = action.strip().lower()
    definition = get_definition(word)
    
    if definition == None:
        await message.reply('could not get definition')
    else:
        embed = Embed(
            title = word,
            color = 0xe8e742
        )
        embed.add_field(
            name = 'definition',
            value = definition
        )
        await message.reply(embed=embed)

    # help
async def help(ctx):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        f'**syntax**: {bot.bot_prefix} dictionary <word>\n'
        '**use**: to search for a definition of <word>'
    )
