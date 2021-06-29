from os import getenv
from dotenv import load_dotenv
import discord

load_dotenv()

class Bot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'what sound does wolfie make?':
            await message.channel.send('In general Wolfie makes these sounds: whimper, whine, growl, rarely bark, howling, moan, yawn, and shrill yaps (bark) Wolfie will howl to signal packs, gather them, warn others, claim territory, before a hunt and after kills, when excited, when mournful, and as a way to socialize.')

wolfie_bot = Bot()
wolfie_bot.run(getenv('bot_token'))
