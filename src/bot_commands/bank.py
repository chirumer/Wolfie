import os
    # os related stuff

def get_database(connection_string):
        # get database object
    from pymongo import MongoClient
    client = MongoClient(connection_string)
    return client['Wolfie']

db = get_database(os.getenv('db_string'))
howls_db = db['howls']

meta = {}
meta['name'] = 'bank'
meta['invoking_keywords'] = ['bank']
meta['description'] = 'this command is not for robbing banks'

async def help(ctx):
    message = ctx['message']
    await message.reply('no help for you')

async def command(ctx, action):

    sub_command = action.split()[0]

    if sub_command == 'create':
        await create_bank(ctx)

    elif sub_command == 'work':
        await work(ctx)

    elif sub_command == 'view':
        await view(ctx)

       
async def create_bank(ctx):
    message = ctx['message']

    if await has_account(message.author.id):
        await message.reply('you already have an account')
    else:
        howls_db.insert_one({'user': message.author.id, 'howls': 100})
        await message.reply('your howling account now has 100 howls')

async def view(ctx):
    message = ctx['message']

    user_account = howls_db.find_one({'user': message.author.id})
    if user_account == None:
        await message.reply('you do not have a howling account')
    else:
        await message.reply(f"you have {user_account['howls']} howls")

async def work(ctx):
    message = ctx['message']

    if not await has_account(message.author.id):
        await message.reply('no account')
    else:
        howls_db.update({'user': message.author.id}, {'$inc': {'howls': 10}})
        await message.reply('rewarded 10 howls for hard work')
 
async def has_account(user):
    user_account = howls_db.find_one({'user': user})
    return user_account != None
