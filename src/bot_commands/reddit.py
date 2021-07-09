#### imports

import os
    # for os related stuff


from src.bot_commands.generic import takes_no_args
    # notify user: command takes no arguments

from src.classes.Subreddit import Subreddit
    # interface to a subreddit of reddit


#### main

def generate_reddit_command(subreddit_name, cmd_name):
    subreddit = Subreddit(subreddit_name, cache_limit=10) # CHANGE CACHE LIMIT
        # subreddit interface
    async def reddit_command(ctx):
            # generated command
        action = ctx['action']

        # called with too many arguments
        if action:
            await takes_no_args(ctx, cmd_name)
            return

        message = ctx['message']
        bot = ctx['bot']
        
        await message.reply(
            await subreddit.random_image()
        )
    return reddit_command


#### exports

print('loading reddit data..')

commands = []

meme_meta = {
    'name': 'meme',
    'aliases': [],
    'description': (
        'view a random meme'
    )
}
meme_command = generate_reddit_command('memes', 'meme')
command = {
    'caller': meme_command,
    'meta': meme_meta
}
commands.append(command)

science_meta = {
    'name': 'science',
    'aliases': [],
    'description': (
        'view a random science related meme'
    )
}
science_command = generate_reddit_command('sciencememes', 'science')
command = {
    'caller': science_command,
    'meta': science_meta
}
commands.append(command)

programming_meta = {
    'name': 'programming',
    'aliases': [],
    'description': (
        'view a programming related meme'
    )
}
programming_command = generate_reddit_command('ProgrammerHumor', 'programming')
command = {
    'caller': programming_command,
    'meta': programming_meta
}
commands.append(command)

print('loaded reddit data')
