async def on_message(self, message):

    # don't respond to ourselves
    if message.author == self.user:
        return

    if message.content == 'hi':
        await message.channel.send('cool')
