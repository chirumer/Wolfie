import asyncio
    # asynchronous programming
from discord import Emoji
    # emoji
from src.database import thanks_db
    # mongodb collection for storing thanks data

thanks_keywords = ['thx', 'thanks', 'thnks', 'thnx', 'thank']
    # what counts as a thanks

async def on_thanks(payload):
    in_session = payload['in_session']
    if in_session:
            # ignore session messages
        return

    message = payload['message']
    bot = payload['bot']

    if message.author.bot:
            # ignore bots
        return

    if not any(word in message.content for word in thanks_keywords):
            # if isn't a thanks message
        return

    thanked_persons = message.mentions
    if message.author in thanked_persons: 
        thanked_persons.remove(message.author)
    if not thanked_persons:
            # not mentioned anyone
        return

    # verify thanks
    timeout = 10

    confirmation = (
        'select ✅ if you meant to thank\n'
        'select ❌ otherwise\n'
    )
    for member in thanked_persons:
        confirmation += f'{member.mention}\n'
    confirmation += f'\n({timeout} seconds to respond)'

    confirmation_message = await message.reply(confirmation)
    confirm = await confirmation_message.add_reaction('✅')
    cancel = await confirmation_message.add_reaction('❌')

    targets = [{
        'user': message.author,
        'message': confirmation_message
    }, {
        'user': message.author,
        'message': confirmation_message
    }]

    async def timeout_caller(message):
        await message.delete()

    async def on_select(ctx):
        reaction = ctx['reaction'].emoji
        
        if reaction == '✅':
            for person in thanked_persons:
                thanks_db.update({'user': person.id}, {'$inc': {'thanks': 1}}, upsert=True)
            await confirmation_message.delete()
            return

        if reaction == '❌':
            # db push
            await confirmation_message.delete()
            return

    bot.add_reaction_session(timeout, targets, on_select, 
        timeout_caller, confirmation_message)
