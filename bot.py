from os import getenv
    # reading env variables
from dotenv import load_dotenv
    # loading env variables from env file
import discord
    # discord API wrapper

import command_handler

load_dotenv()
    # load env variables from env file

class Bot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    on_message = command_handler.on_message

wolfie_bot = Bot()
wolfie_bot.run(getenv('bot_token'))
