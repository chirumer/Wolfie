from src.database import howls_db
    # database
from src.bot_commands.generic import improper_arguments, fix_args
    # respond to improper command arguments

improper_arguments = fix_args(improper_arguments, cmd_name='bank')

    # meta
meta = {}
meta['name'] = 'bank'
meta['invoking_keywords'] = ['bank']
meta['description'] = 'this command is not for robbing banks'

    # wrapper for sub commands
def sub_command(meta=None):
    def internal(func):
        sub_commands.append({
            'name': func.__name__,
            'caller': func,
            'meta': meta
        })
        return func
    return internal

    # main command
async def command(ctx, action):
    if not action:
        await improper_arguments(ctx)
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
        await improper_arguments(ctx)


sub_commands = []

    # help function
cmd_meta = {}
cmd_meta['description'] = 'get help on sub-commands'
@sub_command(cmd_meta)
async def help(ctx, action=None):
    if action:
        await improper_arguments(ctx)
        return

    message = ctx['message']
    bot = ctx['bot']

    help_str = 'Available usages:\n\n'

    for command in sub_commands:
        help_str += (
            f"**{bot.bot_prefix} bank {command['name']}**: "
            f"{command['meta']['description']}\n"
        )

    await message.reply(help_str)

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

    if user_account == None:
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
