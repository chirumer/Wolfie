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

    #  generate help command
help_meta = {}
help_meta['description'] = 'get help on sub-commands'
def generate_generic_help(cmd_name, sub_commands, invalid_caller):
    async def help(ctx, action=None):
        if action:
            await invalid_caller(ctx)
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

    # generate the command handler
def generate_main_command(sub_commands, invalid_caller):
    async def command(ctx, action):
        if not action:
            await invalid_caller(ctx)
            return

        message = ctx['message']
        bot = ctx['bot']

        sub_command = action.split()[0]
        action = action[len(sub_command):].strip()

        for command in sub_commands:
            if command['name'] == sub_command:
                await command['caller'](ctx, action)
                break
        else:
            await invalid_caller(ctx)
    return command

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
