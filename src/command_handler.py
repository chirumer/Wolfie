import json
    # parse json file

config = json.load(open('../config.json'))
    # load config

async def on_message(self, message):

    # don't respond to ourselves
    if message.author == self.user:
        return

    # if user is instructing us
    if message.content.startswith(config['bot_prefix']):
        await handle_command(
            message,
            message.content[len(config['bot_prefix']):].strip()
        )
        return

async def handle_command(ctx, action):

    # if no command specified
    if not action:
        await ctx.reply(
            'No command specified..\n'
            f"**type** {config['bot_prefix']} help\n"
            'for help'
        )
        return

    await ctx.channel.send(f'I have received command: {action}')
