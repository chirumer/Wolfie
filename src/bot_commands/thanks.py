from src.database import thanks_db
    # mongodb collection


#### exports

    # meta
meta = {}
meta['name'] = 'thanks'
meta['invoking_keywords'] = ['thanks']
meta['description'] = 'view the thanks leaderboard'

    # main command
async def command(ctx, action):
    message = ctx['message']
    bot = ctx['bot']

    if action:
        await message.reply(
            'this command takes no arguments..\n'
            f'**type** {bot.bot_prefix} help\n'
            'for help'
        )
        return

    leaderboard = 'top 10 thanked:\n\n'

    leaders = thanks_db.find().sort('thanks', -1).limit(10)

    for index, leader in enumerate(leaders):
        user = await bot.fetch_user(leader['user'])
        leaderboard += (
            f'({index+1}) '
            f"{user.mention}: "
            f"{leader['thanks']}\n"
        )

    leaderboard += (
        '\nwhat is considered as a thank: '
        'user mentions the person being thanked in a message '
        'which contains a keyword like thanks'
    )

    await message.reply(leaderboard)
