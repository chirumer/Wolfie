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

help_meta = {}
help_meta['description'] = 'get help on sub-commands'
async def generic_help(ctx, cmd_name, sub_commands):
    message = ctx['message']
    bot = ctx['bot']

    help_str = 'available usages:\n\n'

    for command in sub_commands:
        help_str += (
            f"**{bot.bot_prefix} {cmd_name} {command['name']}**: "
            f"{command['meta']['description']}\n"
        )

    await message.reply(help_str)
