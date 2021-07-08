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

def generate_reddit_command(subreddit_name):
    subreddit = Random_image(subreddit_name)
    async def reddit_command(ctx, action):
        message = ctx['message']
        bot = ctx['bot']

        if action:
            await takes_no_args(ctx)

        await message.reply(await subreddit.random_image())
    return reddit_command

### exports

print('loading reddit data..')

metas = []
commands = []

    # meme
meme_meta = {}
meme_meta['name'] = 'meme'
meme_meta['invoking_keywords'] = ['meme']
meme_meta['description'] = 'view a random meme'
metas.append(meme_meta)
meme_command = generate_reddit_command('memes')
commands.append(meme_command)

    # science
science_meta = {}
science_meta['name'] = 'science'
science_meta['invoking_keywords'] = ['science']
science_meta['description'] = 'view a random science related meme'
metas.append(science_meta)
science_command = generate_reddit_command('sciencememes')
commands.append(science_command)

    # programming
programming_meta = {}
programming_meta['name'] = 'programming'
programming_meta['invoking_keywords'] = ['programming']
programming_meta['description'] = 'view a random programming meme'
metas.append(programming_meta)
programming_command = generate_reddit_command('ProgrammerHumor')
commands.append(programming_command)

print('done')


async def takes_no_args(ctx):
    message = ctx['message']
    bot = ctx['bot']

    message.reply (
        'this command takes no arguments..\n'
        f'**type** {bot.bot_prefix} help\n'
        'for help'
    )
