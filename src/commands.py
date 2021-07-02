commands = []

# decorator to add command to list
def bot_command(meta):

    def command(func):
        for invoking_keyword in meta['invoking_keywords']:
            commands.append({
                'command_name': invoking_keyword,
                'callback': func,
                'meta': meta
            })

    return command

    # hi command
meta = {}
meta['invoking_keywords'] = ['hi']
meta['name'] = 'hi'
meta['description'] = 'bot says hi'

@bot_command(meta)
async def hi_command(ctx, action):
    await ctx.reply('hi')

    # help command
meta = {}
meta['invoking_keywords'] = ['help']
meta['name'] = 'help'
meta['description'] = 'bot commands usage info'

@bot_command(meta)
async def help_command(ctx, action):

    help_str = '**Available commands:**'
    help_str += "\n"
    for command in commands:
        help_str += f"\n**{command['meta']['name']}**"
        help_str += f": {command['meta']['description']}"
    help_str += (
            '\n\nFor information on a particular command type: '
            '**help {command name}**'
    )

    await ctx.channel.send(help_str)
