#### imports

import urllib.request
    # to make HTTP request

import re
    # for regular expressions


from src.bot_commands.generic import too_few_args
    # notify user: command requires more arguments


#### exports

    # meta
meta = {
    'name': 'youtube',
    'aliases': [],
    'description': (
        'quickly get a youtube link for a topic'
    )
}

    # main command
async def command(ctx):

    search_phrase= ctx['action']
    if not search_phrase:
        await too_few_args(ctx, 'youtube', 1)
        return

    # replace whitespace with +
    search_phrase = re.sub(r'\s+', '+', search_phrase)

    # get links
    html = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + search_phrase
    )
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    links = [
        'https://www.youtube.com/watch?v=' + video_id
        for video_id in video_ids
    ]

    # display to user
    message = ctx['message']
    await message.reply(
        'Here are some links:\n'
        + links[0] + '\n'
        + links[1] + '\n'
        + links[2]
    )

    # help
async def help(ctx):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        f'**syntax**: {bot.bot_prefix} youtube <search phrase>\n'
        '**use**: to quickly get a youtube link for a topic'
    )

####
# TO DO
# -> use arrow emojis to scroll through links
