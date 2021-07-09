#### imports

from src.bot_commands.generic import takes_no_args
    # for notifying user: command takes no arguments


#### exports

    # meta
meta = {
    'name': 'test',
    'aliases': [],
    'description': (
        'testing..'
    )
}

    # main command
async def command(ctx):
    action = ctx['action']
    message = ctx['message']
    bot = ctx['bot']

    async def func1():
        await message.reply('hi')
        return

    target = {
        'user': message.author.id,
        'channel': message.channel.id
    }

    await bot.add_message_session(15, target, func1, func1)
