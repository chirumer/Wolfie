from src.database import howls_db
    # database
from src.bot_commands.generic import ( 
    improper_arguments, fix_args, 
    generate_generic_help, help_meta, 
    generate_sub_command_wrapper,
    generate_main_command
) # generic stuff

sub_commands = []

sub_command = generate_sub_command_wrapper(sub_commands)
improper_arguments = fix_args(improper_arguments, cmd_name='bank')

#### exports

    # meta
meta = {}
meta['name'] = 'bank'
meta['invoking_keywords'] = ['bank']
meta['description'] = 'this command is not for robbing banks'

    # main command
command = generate_main_command(sub_commands, improper_arguments)

    # help function
help = generate_generic_help('bank', sub_commands, improper_arguments)
help = sub_command(help_meta)(help)

#### sub commands

    # create
cmd_meta = {}
cmd_meta['description'] = 'create a howling account'
@sub_command(cmd_meta)
async def create(ctx, action):
    if action:
        await improper_arguments(ctx)
        return

    message = ctx['message']

    reply = ''

    if await has_account(message.author.id):
        reply = 'you already have a howling account'
    else:
        howls_db.insert_one({'user': message.author.id, 'howls': 100})
        reply = 'created new howling account'

    await message.reply(reply)

    # view
cmd_meta = {}
cmd_meta['description'] = 'view howling account balance'
@sub_command(cmd_meta)
async def view(ctx, action):
    if action:
        await improper_arguments(ctx)
        return

    message = ctx['message']

    user_account = howls_db.find_one({'user': message.author.id})
    reply = ''

    if user_account == none:
        reply = 'you do not have a howling account'
    else:
        reply = f"you have {user_account['howls']} howls"
    await message.reply(reply)

    # work
cmd_meta = {}
cmd_meta['description'] = 'work and earn howls'
@sub_command(cmd_meta)
async def work(ctx, action):
    if action:
        await improper_arguments(ctx)
        return

    message = ctx['message']
    reply = ''

    if not await has_account(message.author.id):
        reply = 'you need a howling account to work'
    else:
        howls_db.update({'user': message.author.id}, {'$inc': {'howls': 10}})
        reply = 'rewarded 10 howls for hard work'
    await message.reply(reply)
 
async def has_account(user):
    user_account = howls_db.find_one({'user': user})
    return user_account != None
