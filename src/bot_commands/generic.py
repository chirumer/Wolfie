async def improper_arguments(ctx, cmd_name):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        'Improper command arguments..\n'
        f'**type** {bot.bot_prefix} help {cmd_name}\n'
        'for help'
    )

def fix_args(func, *args, **kwargs):
    async def fixed(ctx):
        await func(ctx, *args, **kwargs)
    return fixed
