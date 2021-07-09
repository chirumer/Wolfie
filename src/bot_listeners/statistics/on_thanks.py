#### imports

from src.database import thanks_db
    # mongodb collection for storing thanks data


#### main

thanks_keywords = ['thx', 'thanks', 'thnks', 'thnx', 'thank']
    # what counts as a thanks

    # main listener
async def listener(ctx):
    in_session = ctx['in_session']
    is_command = ctx['is_command']
    message = ctx['message']
    bot = ctx['bot']


    #### callers

    async def timeout_caller():
        await confirmation_message.delete()

    async def on_reacted(ctx):
        emoji = ctx['reaction'].emoji

        if emoji == '✅':

            # update database
            for user in thanked_users:
                thanks_db.update(
                    {
                        'user': user.id
                    }, 
                    {
                        '$inc': {
                            'thanks': 1
                        }
                    },
                    upsert = True
                )

            # notify success
            if len(thanked_users) == 1:
                await message.reply('user has been thanked')
            else:
                await message.reply('users have been thanked')

        elif emoji == '❌':
            await confirmation_message.delete()


    #### main

    if in_session or is_command or message.author.bot:
            # not our bussiness
        return

    if not any(word in message.content for word in thanks_keywords):
            # not a thanks message
        return

    # who the message thanks
    thanked_users = [
        user for user in message.mentions
        if 
        not user.bot and user != message.author
    ]

    if not thanked_users:
            # nobody is being thanked
        return

    # time for user to confirm thanks
    timeout = 10 
        # 10 seconds

    # construct confirmation message
    confirmation = (
        'select ✅ if you meant to thank\n'
        'select ❌ otherwise\n'
        'users being thanked:\n'
    )
    for user in thanked_users:
        confirmation += f'{user.mention}\n'
    confirmation += f'\n({timeout} seconds to respond)'

    # prompt confirmation
    confirmation_message = await message.reply(confirmation)

    # construct session targets
    targets = [{
        'user': message.author.id,
        'message': confirmation_message.id,
        'emoji': '✅'
    }, {
        'user': message.author.id,
        'message': confirmation_message.id,
        'emoji': '❌'
    }]
    # add session
    await bot.add_emoji_session(
        timeout, 
        targets, 
        on_reacted, 
        timeout_caller
    )

    # prompt reactions
    await confirmation_message.add_reaction('✅')
    await confirmation_message.add_reaction('❌')
