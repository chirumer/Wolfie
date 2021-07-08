import asyncpraw
    # reddit API wrapper
import os
    # os related stuff
import asyncio
    # asynchronous programming

reddit = asyncpraw.Reddit(
    client_id = os.getenv('reddit_client'),
    client_secret = os.getenv('reddit_secret'),
    user_agent = 'linux:WolfieBot:0.1 (by u/broadent)'
)

async def get_subreddits():
    global memes
    memes = await reddit.subreddit('memes')

loop = asyncio.get_event_loop()
loop.run_until_complete(get_subreddits())

### exports

    # meme

meme_meta = {}
meme_meta['name'] = 'meme'
meme_meta['invoking_keywords'] = ['meme']
meme_meta['description'] = 'view a random meme'

async def meme_command(ctx, action):
    message = ctx['message']
    bot = ctx['bot']

    if action:
        await takes_no_args(ctx)

    sent_message = await message.reply('loading')

    meme = (await memes.random()).url
    await sent_message.edit(content=meme)



async def take_no_args(ctx):
    message = ctx['message']
    bot = ctx['bot']

    message.reply (
        'this command takes no arguments..\n'
        f'**type** {bot.bot_prefix} help\n'
        'for help'
    )
