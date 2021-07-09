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

# generate main command
def generate_main_command(sub_commands, cmd_name):
    async def command(ctx):
        action = ctx['action']
        if not action:
            await too_few_args(ctx, cmd_name, 1)
            return

        action = ctx['action']
        invoked_command = action.split()[0]
        ctx['action'] = action[len(invoked_command):].strip()

        for command in sub_commands:
            if command['name'] == invoked_command:
                await command['caller'](ctx)
                break
        else:
            message = ctx['message']
            bot = ctx['bot']
            await message.reply(
                'no such sub command..\n'
                f'**type** {bot.bot_prefix} help {cmd_name}\n'
                f'for help with {cmd_name} command'
            )

    return command

# generate help command
help_meta = {
    'description': 'get help on sub-commands'
}
def generate_help_command(sub_commands, cmd_name):
    async def help(ctx):
        action = ctx['action']
        if action:
            await too_many_args(ctx, cmd_name, 1)
            return

        message = ctx['message']
        bot = ctx['bot']

        help_str = 'available usages:\n\n'

        for command in sub_commands:
            help_str += (
                f"**{bot.bot_prefix} {cmd_name} {command['name']}**: "
                f"{command['meta']['description']}\n"
            )

        await message.reply(help_str)

    return help
