import praw
    # reddit API wrapper
import os
    # os related stuff
import asyncio
    # asynchronous programming

reddit = praw.Reddit(
    client_id = os.getenv('reddit_client'),
    client_secret = os.getenv('reddit_secret'),
    user_agent = 'linux:WolfieBot:0.1 (by u/broadent)',
    check_for_async = False
)

class Random_image():

    def __init__(self, subreddit_name, cache_limit=10):
        self._subreddit = reddit.subreddit(
            subreddit_name
        )
        self._images = []
        self._cache_limit = cache_limit
        self._lock = asyncio.Lock()

        while len(self._images) < self._cache_limit:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._add_image())

    async def _add_image(self):
        self._images.append(
            self._subreddit.random().url
        )

    async def random_image(self):

        # lock to prevent popping empty list
        async with self._lock:
            while not self._images:
                asyncio.sleep(1)

            asyncio.create_task(self._add_image())

            return self._images.pop()


print('loading reddit data')
memes = Random_image('memes', cache_limit=5)
print('done')

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

    meme = await memes.random_image()
    await message.reply(meme)


async def take_no_args(ctx):
    message = ctx['message']
    bot = ctx['bot']

    message.reply (
        'this command takes no arguments..\n'
        f'**type** {bot.bot_prefix} help\n'
        'for help'
    )
