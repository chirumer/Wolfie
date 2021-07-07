# if non-existent command
async def default_command(ctx):
    message = ctx['message']
    bot = ctx['bot']

    reply_str = ''
    reply_str += 'Unknown_command!'
    reply_str += f'\n**type:** {bot.bot_prefix} help'
    reply_str += '\nfor help'

    await message.reply(reply_str)

commands = []
    # list of all commands

# function to add command to list
def make_command(func, meta, help_cmd=None):
    for invoking_keyword in meta['invoking_keywords']:
        commands.append({
            'command_name': invoking_keyword,
            'callback': func,
            'meta': meta,
            'help_command': help_cmd
        })


    # hi command
import src.bot_commands.hi as hi
make_command(hi.command, hi.meta)

    # thanks command
import src.bot_commands.thanks as thanks
make_command(thanks.command, thanks.meta)

    # reading command
import src.bot_commands.reading as reading
make_command(reading.command, reading.meta, reading.help)

    # bank command
import src.bot_commands.bank as bank
make_command(bank.command, bank.meta, bank.help)

    # help command
help_meta = {}
help_meta['invoking_keywords'] = ['help']
help_meta['name'] = 'help'
help_meta['description'] = 'bot commands usage info'

async def help_command(ctx, action):
    message = ctx['message']
    bot = ctx['bot']

    if not action:

        help_str = '**Available commands:**'
        help_str += "\n"
        for command in commands:
            help_str += f"\n**{command['meta']['name']}**"
            help_str += f": {command['meta']['description']}"
        help_str += (
                '\n\nFor information on a particular command type: '
                '**help {command name}**'
        )
        await message.channel.send(help_str)
        return

    specified_command = action.split()[0]

    if action[len(specified_command):].strip():
        await message.reply(
            'Invalid syntax..\n'
            f'**type** {bot.bot_prefix} help\n'
            'for help'
        )
        return

    for command in commands:
        if command['command_name'] == specified_command:
            if not command['help_command']:
                await message.reply('this command does not implement a help action')
                return
            await command['help_command'](ctx)
            return

    await message.reply(
        'no such command..\n'
        f'**type** {bot.bot_prefix} help\n'
        'for help'
    )

make_command(help_command, help_meta)
