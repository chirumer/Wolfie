    # message for user
async def improper_arguments(ctx, cmd_name):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        'Improper command arguments..\n'
        f'**type** {bot.bot_prefix} help {cmd_name}\n'
        'for help'
    )

    # helper
def fix_args(func, *args, **kwargs):
    async def fixed(ctx):
        await func(ctx, *args, **kwargs)
    return fixed

    # generic help command
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

    # generate wrapper for sub commands
def generate_sub_command_wrapper(sub_commands):
    def sub_command(meta=None):
        def internal(func):
            sub_commands.append({
                'name': func.__name__,
                'caller': func,
                'meta': meta
            })
            return func
        return internal
    return sub_command
