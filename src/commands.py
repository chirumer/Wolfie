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
def make_command(func, meta):
    for invoking_keyword in meta['invoking_keywords']:
        commands.append({
            'command_name': invoking_keyword,
            'callback': func,
            'meta': meta
        })


    # hi command
import src.bot_commands.hi as hi
make_command(hi.command, hi.meta)


    # help command
help_meta = {}
help_meta['invoking_keywords'] = ['help']
help_meta['name'] = 'help'
help_meta['description'] = 'bot commands usage info'

async def help_command(ctx, action):
    message = ctx['message']

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

make_command(help_command, help_meta)
