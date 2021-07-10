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
