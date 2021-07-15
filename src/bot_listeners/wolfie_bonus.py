#### imports

import random
    # random selection


from src.database import howls_db
    # mongodb collection for howling bank account


#### constants

lowest_bonus = 1
highest_bonus = 5
chance_per_thousand = 100


#### main

async def listener(ctx):
    # only for bot commands
    is_command = ctx['is_command']
    if not is_command:
        return

    if random.randint(1,1000) > chance_per_thousand:
        # no bonus
        return

    reward = random.randint(lowest_bonus, highest_bonus)

    message = ctx['message']
    ensure_account(message.author.id)
    howls_db.update({
        'user': message.author.id
    }, {
        '$inc': {
            'howls': reward
        }
    })
    await message.reply(
        '**wolfie bonus**!!\n'
        f'{message.author.mention} has been rewarded with '
        f'**{reward}** howls to their howling bank account!\n'
        'Keep using wolfie for more rewards!'
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
