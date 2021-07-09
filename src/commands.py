#### imports

from discord import Embed
    # for making embedded messages


from src.bot_commands.generic import too_many_args
    # notifty user: too many arguments


#### exports

commands = []
    # list of all commands


#### main

async def default_help(ctx):
        # notifty user: help not implemented
    message = ctx['message']
    await message.reply(
        'this command does not implement '
        'a help action'
    )

# function to make command
def make_command(caller, meta, help_cmd = default_help):

    # add to commands
    name = meta.pop('name')
    aliases = meta.pop('aliases')
    commands.append({
        'name': name,
        'aliases': aliases,
        'caller': caller,
        'meta': meta,
        'help': help_cmd
    })


#### commands

    # test command
#import src.bot_commands.test as test
#make_command(test.command, test.meta)

    # hi command
import src.bot_commands.hi as hi
make_command(hi.command, hi.meta)

    # thanks command
import src.bot_commands.thanks as thanks
make_command(thanks.command, thanks.meta)

    # dictionary command
import src.bot_commands.dictionary as dictionary
make_command(dictionary.command, dictionary.meta, dictionary.help)

    # reading command
import src.bot_commands.reading as reading
make_command(reading.command, reading.meta, reading.help)

# reddit commands
from src.bot_commands.reddit import (
    commands as reddit_commands
)
for command in reddit_commands:
    make_command(command['caller'], command['meta'])

    # help command
help_meta = {
    'name': 'help',
    'aliases': [],
    'description': (
        'use this command for a brief '
        'overview of the available commands, '
        'and for help with specific commands.'
    )
}
misc_info = [
    {
        'title': 'thanks counter',
        'description': (
            'The bot keeps track of how many times '
            'a user has been thanked. '
            '**What counts**: the user being thanked '
            'must be mentioned in a message containing '
            'a keyword like thanks. '
            '**thanks** command can be used to view the '
            'thanks leaderboard'
        )
    }
]
async def help_command(ctx):
    message = ctx['message']
    bot = ctx['bot']
    action = ctx['action']

    if not action:
            # no arguments

            # display general help

        # construct command embed
        cmds_embed = Embed(
            title = "AVAILABLE COMMANDS", 
            color = 0xe8e742
        )
        for command in commands:
            cmds_embed.add_field(
                name = command['name'],
                value = (
                    (
                        command['meta']['description']
                        + '\n**aliases**: '
                        + ', '.join(command['aliases'])
                    )
                    if command['aliases']
                    else
                    command['meta']['description']
                ),
                inline = False
            )

        # construct miscellanious embed
        misc_embed = Embed(
            title = "MISCELLANIOUS INFO",
            color =  0xe8e742
        )
        for misc in misc_info:
            misc_embed.add_field(
                name = misc['title'],
                value = misc['description']
            )

        await message.reply(embed = cmds_embed)
        await message.reply(embed = misc_embed)
        return

    if len(action.split()) > 1:
            # too many arguments
        await too_many_args(ctx, 'help', 1)
        return

    # the command for which user requires help
    target_command = action.split()[0]

    for command in commands:
        if command['name'] == target_command:
            if command['help'] == None:
                    # does not impleement help command
                await message.reply(
                    'this command does not implement a help action'
                )
                return
            else:
                await command['help'](ctx)
                return
    else:
        await message.reply(
            'no such command..\n'
            f'**type** {bot.bot_prefix} help\n'
            'for a list of available commands'
        )
        return

make_command(help_command, help_meta)
