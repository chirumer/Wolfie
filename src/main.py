#### imports

import json
    # for working with json data


#### main

# load bot config
bot_config = json.load(open('./bot_config.json'))

# create wolfie
from src.classes.Bot import Bot
wolfie_bot = Bot(
    bot_prefix = bot_config['bot_prefix']
)

# add bot commands
from src.commands import commands
wolfie_bot.add_commands(commands)

# add message listeners
from src.listeners import message_listeners
wolfie_bot.add_message_listeners(message_listeners)




# testing 

async def listener1():
    print('listener1 called')

async def listener2(ctx):
    message = ctx['message']
    action = '2 ' + ctx['action']

    await message.reply(action)

async def listener3(ctx):
    message = ctx['message']
    action = '3 ' + ctx['action']

    await message.reply(action)

wolfie_bot._command.add_listener('wow', listener1);
id = wolfie_bot._command.add_listener('wow', listener2);
wolfie_bot._command.add_listener('wow', listener3);
wolfie_bot._command.add_listener('ok', listener2);
wolfie_bot._command.remove_listener(id)
wolfie_bot._command.remove_all_listeners('ok')
