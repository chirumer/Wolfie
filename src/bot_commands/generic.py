def help_str(bot_prefix, cmd_name):
    return (
        f'**type** {bot_prefix} help {cmd_name}\n'
        f'for help on the {cmd_name} command'
    )

async def takes_no_args(ctx, cmd_name):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        'incorrect syntax..\n'
        'this command takes no arguments.\n'
        + help_str(bot.bot_prefix, cmd_name)
    )

async def too_many_args(ctx, cmd_name, max_args):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        'too many arguments..\n'
        f'this command takes at most {max_args} '
        + (
            'argument.\n'
            if max_args == 1
            else
            'arguments.\n'
        )
        + help_str(bot.bot_prefix, cmd_name)
    )

async def too_few_args(ctx, cmd_name, min_args):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        'too few arguments..\n'
        f'this command takes at least {min_args} '
        + (
            'argument.\n'
            if min_args == 1
            else
            'arguments.\n'
        )
        + help_str(bot.bot_prefix, cmd_name)
    )
