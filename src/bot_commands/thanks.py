#### imports

from src.database import thanks_db
    # is a mongodb database collection

from src.bot_commands.generic import takes_no_args


#### exports

    # meta
meta = {
    'name': 'thanks',
    'aliases': [],
    'description': (
        'view the thanks leaderboard'
    )
}

    # main command
async def command(ctx):
    action = ctx['action']

    # called with too many args
    if action:
        await takes_no_args(ctx, 'thanks')
        return

    message = ctx['message']
    bot = ctx['bot']

    # get top 10 thanked
    leaders = thanks_db.find().sort('thanks', -1).limit(10)

    # construct leaderboard string
    leaderboard ='top 10 thanked:\n\n'
    for position, leader in enumerate(leaders, 1):
        user = await bot.fetch_user(leader['user'])
        leaderboard += (
            f'({position}) '
            f'{user.mention}: '
            f"{leader['thanks']}\n"
        )
    leaderboard += (
        '\nwhat is considered as a thank: '
        'user mentions the person being thanked in a message '
        'which contains a keyword like thanks'
    )
    await message.reply(leaderboard)
