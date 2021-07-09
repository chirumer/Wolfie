#### imports

from src.bot_commands.generic import takes_no_args
    # for notifying user: command takes no arguments


#### exports

    # meta
meta = {
    'name': 'hi',
    'aliases': ['hello', 'hey'],
    'description': (
        'wolfie says hi'
    )
}

    # main command
async def command(ctx):
    action = ctx['action']
    
    # called with too many args
    if action:
        await takes_no_args(ctx, 'hi')
        return

    # say hi
    message = ctx['message']
    await message.reply('*sniff*')
