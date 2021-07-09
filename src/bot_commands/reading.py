#### imports

from datetime import datetime, timedelta
    # time handling

import csv
    # csv manipulation

import random
    # random selection

from src.bot_commands.generic import takes_no_args
    # notify user: command takes no arguments


#### initialize


books = []

with open('assets/books/meta.csv') as meta_file:

    csv_reader = csv.reader(meta_file, delimiter=',')
    books_directory = next(csv_reader)[0]

    for book_title, book_path, no_lines in csv_reader:
        book = {
            'title': book_title,
            'book': open(f'assets/books/{books_directory}/{book_path}'),
            'no_lines': int(no_lines)
        }
        books.append(book)


#### exports

    # meta
meta = {
    'name': 'reading',
    'aliases': [],
    'description': (
        'check your reading speed'
    )
}

    # main command
async def command(ctx):

    # globals

    last_sent_message = None
    words_read = 0
    time_taken = timedelta()

    last_para_words = None
    start_time = None

    from_books = set()

    # helper functions

    def get_para(no_lines):

        # choose random book
        chosen_book = random.choice(books)

        # choose random para
        para = ''
        random_start = random.randrange(chosen_book['no_lines']-no_lines)
        for i in range(random_start-1):
            chosen_book['book'].readline()
        for i in range(no_lines):
            para += chosen_book['book'].readline()

        # reset file pointer
        chosen_book['book'].seek(0)

        return para, chosen_book['title']

    # return string containing reading speed
    def reading_speed_str():
        if words_read == 0:
            return 'no data to calculate reading speed'

        reading_speed = (words_read / time_taken.total_seconds())*60
        reading_speed = round(reading_speed, 2)

        return (
            f"{message.author.mention}'s reading speed: **{reading_speed}**\n"
            "you read excerpts from:\n"
            + '**' + "\n".join(from_books) + '**'
        )

    # called when user times out
    async def timeout_caller():

        # construct timeout message
        timeout_message = (
            'late reply..\n'
            'aborted'
        )

        # append reading speed if at least one para shown
        if last_sent_message != instructions_message:
            timeout_message += '\n\n'
            timeout_message += (
                reading_speed_str()
            )

        # display timeout message
        await message.channel.send(timeout_message)


    async def next_para(ctx):
        emoji = ctx['reaction'].emoji

        # non locals
        nonlocal timeout
        nonlocal last_sent_message, words_read, time_taken
        nonlocal last_para_words, start_time
        nonlocal from_books

        # game aborted
        if emoji == '❌':
            # user has not played
            if last_sent_message == instructions_message:
                await message.channel.send('game aborted by user')
                return
            # construct reading speed message
            aborted_str = (
                'game stopped by user..\n'
                '**note**: aborted para not counted in calculation\n\n'
                +
                reading_speed_str()
            )
            await message.channel.send(aborted_str)
            return

        assert emoji == '✅', 'unexpected emoji received'


        # if there is data to append
        if last_sent_message != instructions_message:
            time_taken += datetime.now() - start_time
            words_read += last_para_words

        # para to send
        para, book = get_para(5)
        from_books.add(book)
        warning = f'\n\n({timeout} seconds timeout)'

        # display para
        last_sent_message = await message.channel.send(para + warning)

        # update current session data
        last_para_words = len(para.split())
        start_time = datetime.now()

        # construct session targets
        targets = [{
            'user': message.author.id,
            'message': last_sent_message.id,
            'emoji': '✅'
        }, {
            'user': message.author.id,
            'message': last_sent_message.id,
            'emoji': '❌'
        }]
        # add session
        await bot.add_emoji_session(
            timeout, 
            targets, 
            next_para, 
            timeout_caller
        )

        # prompt reactions
        await last_sent_message.add_reaction('✅')
        await last_sent_message.add_reaction('❌')


    # main

    action = ctx['action']

    # called with too many args
    if action:
        await takes_no_args(ctx, 'reading')

    message = ctx['message']
    bot = ctx['bot']

    # timeout for prompts
    timeout = 60 * 2
        # 2 minutes
    # timeout for instructions prompt
    instructions_timeout = 30
        # 30 seconds

    # instructions to play the game
    instruction = (
        "**Let's play a game..**\n"
        'You will be given a paragraph. '
        'Press the ✅ reaction after FULLY reading the paragraph. '
        'A new paragraph will be loaded for reading. '
        'Press the ❌ reaction when you want to stop reading.'
        '\n\nPress ✅ to begin!\n'
        f'({instructions_timeout} seconds timeout)'
    )

    # display instructions
    instructions_message = await message.reply(instruction)
    last_sent_message = instructions_message

    # construct session targets
    targets = [{
        'user': message.author.id,
        'message': instructions_message.id,
        'emoji': '✅'
    }, {
        'user': message.author.id,
        'message': instructions_message.id,
        'emoji': '❌'
    }]
    # add session
    await bot.add_emoji_session(
        instructions_timeout, 
        targets, 
        next_para, 
        timeout_caller
    )

    # prompt reactions
    await instructions_message.add_reaction('✅')
    await instructions_message.add_reaction('❌')


    # help
async def help(ctx):
    message = ctx['message']
    bot = ctx['bot']

    await message.reply(
        f'**syntax**: {bot.bot_prefix} reading\n'
        '**use**: to start reading game'
    )
