#### imports

from src.database import howls_db
    # mongodb collection for storing howls information

from src.bot_commands.generic import (
    generate_sub_command_wrapper,
    generate_main_command,
    generate_help_command, help_meta,
    too_many_args
)


#### constants

# amount of howls in new howling bank accounts
starting_balance = 100


#### main

sub_commands = []

sub_command = generate_sub_command_wrapper(sub_commands)


#### exports

    # meta
meta = {
    'name': 'bank',
    'aliases': [],
    'description': (
        'commands related to your howling bank account'
    )
}

    # main command
command = generate_main_command(sub_commands, 'bank')

    # help function
help = generate_help_command(sub_commands, 'bank')
help = sub_command(help_meta)(help)


#### sub commands

    # view
cmd_meta = {
    'description': 'view your howling bank account balance'
}
@sub_command(cmd_meta)
async def view(ctx):
    action = ctx['action']
    if action:
        await too_many_args(ctx, 'bank', 1)
        return

    message = ctx['message']

    ensure_account(message.author.id)
    account = howls_db.find_one({'user': message.author.id})

    balance = account['howls']

    await message.reply(
        f'Your howling account balance: **{balance}** howls\n'
    )

    # earn
cmd_meta = {
    'description': 'earn howls to add to your howling bank account'
}
@sub_command(cmd_meta)
async def earn(ctx):
    action = ctx['action']
    if action:
        await too_many_args(ctx, 'bank', 1)
        return

    message = ctx['message']

    await message.reply(
        'currently the only way to earn howls is by **wolfie bonus**. '
        'It is a small amount of howls rewarded randomly '
        'when a user is uses a bot command.'
    )


#### helper functions


# ensures that howling bank account exists
def ensure_account(user):
    acc = howls_db.find_one({'user': user})
    if acc == None:
        howls_db.insert_one({
            'user': user,
            'howls': starting_balance
        })
