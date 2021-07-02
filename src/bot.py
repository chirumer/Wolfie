from os import getenv
    # reading env variables
from dotenv import load_dotenv
    # loading env variables from env file
import discord
    # discord API wrapper
import json
    # parse json file
import asyncio
    # asynchronous programming

load_dotenv()
    # load env variables from env file

config = json.load(open('../config.json'))
    # load config


class Command_handler():
    # handles command events

    def __init__(self):
        self._listeners = []

    # add listener
    def add_listener(self, event, callback):
        self._listeners.append({
            'event': event,
            'callback': callback
        })

    # remove listeners
    def remove_listener(self, event):
        self._listeners = (
            [x for x in self._listeners if x['event'] != event]
        )

    # call listeners
    def emit(self, event, ctx, action):
        for listener in self._listeners:
            if listener['event'] == event:
                asyncio.create_task(
                    listener['callback'](ctx, action)
                )


class Bot(discord.Client):

    def __init__(self, bot_prefix):
        discord.Client.__init__(self)
        self.bot_prefix = bot_prefix
        self.command_handler = Command_handler()

    
    def add_commands():
        pass


    # notify that we've connected
    async def on_ready(self):
        print('Logged on as', self.user)


    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return

        # if user is instructing us
        if message.content.startswith(self.bot_prefix):

            command = (
                message.content[len(self.bot_prefix):].split()
                    and message.content[len(self.bot_prefix):].split()[0]
            )

            if not command:

                # incomplete command
                await message.reply(
                    'No command specified..\n'
                    f"**type** {self.bot_prefix} help\n"
                    'for help'
                )
            else:
                action = message.content[len(self.bot_prefix):].strip()
                self.command_handler.emit(command, message, action)


wolfie_bot = Bot(config['bot_prefix'])
wolfie_bot.run(getenv('bot_token'))
