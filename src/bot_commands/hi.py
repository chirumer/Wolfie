from src.bot_commands.generic import (
    improper_arguments, fix_args
)

improper_arguments = fix_args(
    improper_arguments, cmd_name='hi'
)

#### exports

    # meta
meta = {}
meta['name'] = 'hi'
meta['invoking_keywords'] = ['hi']
meta['description'] = 'wolie says hi'

    # main command
async def command(ctx, action):
    if action:
        await improper_arguments(ctx)
        return
    message = ctx['message']
    await message.reply('*growls*')
