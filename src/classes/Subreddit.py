#### imports

import praw
    # is a Reddit API wrapper library

import os
    # for os related stuff

import asyncio
    # for asynchronous programming


#### class definition

class Subreddit():
        # interface to a subreddit in reddit

    # constructor
    def __init__(self, name, cache_limit=10):
        self._subreddit = reddit.subreddit(name)
            # praw's subreddit interface
        self._images = []
            # cache images for random_image()
        self._cache_limit = cache_limit
            # maximum cache
        self._lock = asyncio.Lock()
            # for preventing race conditions

        while len(self._images) < self._cache_limit:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._add_image())

    # add image to cache
    async def _add_image(self):
        self._images.append(
            self._subreddit.random().url
        )

    async def random_image(self):

        # lock to prevent race condition
        async with self._lock:

            # if no image in cache, wait
            while not self._images:
                asyncio.sleep(1)

            # re-fill the cache later
            asyncio.create_task(self._add_image())

            # give image from cache
            return self._images.pop()


#### internal

# reddit interface
reddit = praw.Reddit(
    client_id = os.getenv('reddit_client'),
    client_secret = os.getenv('reddit_secret'),
    user_agent = 'linux:WolfieBot:0.1 (by u/broadent)',
    check_for_async = False
) 
