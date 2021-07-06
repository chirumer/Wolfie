from datetime import datetime, timedelta
    # working with time
import random
    # random selection
from src.bot_commands.generic import (
    improper_arguments, fix_args,
    generate_generic_help, help_meta,
    generate_sub_command_wrapper,
    generate_main_command
) # generic stuff

sub_commands = []

sub_command = generate_sub_command_wrapper(sub_commands)
improper_arguments = fix_args(improper_arguments, cmd_name='reading')

reading_file = open('assets/harry_potter.txt')
# TO CHANGE
# bot must select a book from multiple books
# optionally get book from the internet
# more processing (don't cut off sentences)
# tell user "excerpts from book .." at end

#### exports

    #meta
meta = {}
meta['name'] = 'reading'
meta['invoking_keywords'] = ['reading']
meta['description'] = 'check your reading speed'

    # main command
command = generate_main_command(sub_commands, improper_arguments)

    # help function
help = generate_generic_help('reading', sub_commands, improper_arguments)
help = sub_command(help_meta)(help)

#### sub commands

    # stats
cmd_meta = {}
cmd_meta['description'] = 'view reading speed stats (yours/general)'
@sub_command(cmd_meta)
async def stats(ctx):
    message = ctx['message']
    await message.reply('not implemented')

    # start
cmd_meta = {}
cmd_meta['description'] = 'check your reading speed'
@sub_command(cmd_meta)
async def start(ctx):
    message = ctx['message']
    bot = ctx['bot']
    user = message.author

    async def timeout(ctx, payload):
        message = ctx['message']

        await message.reply('late reply.. stopped')
        if payload:
            await message.channel.send(
                    interpret(payload, user.mention)
            )

    async def instructions():

        instructions = (
            'You will be given short paragraphs of text\n'
            'type **ok** after reading a paragraph FULLY\n'
            'type **stop** to stop loading new paragraphs\n'
            'type **ready** to begin!'
        )

        return await message.reply(instructions)

    instructions_message = await instructions()

    async def on_ready(ctx, payload):
        message = ctx['message']

        if message.content != 'ready':
            await message.reply('expected **ready**.. aborting')
            return

        def get_para():
            lines_in_para = 5
            no_lines = int(reading_file.readline())

            random_start = random.randrange(0, no_lines-lines_in_para)
            for i in range(random_start-1):
                reading_file.readline()

            para = ''
            for i in range(lines_in_para):
                para += reading_file.readline()

            reading_file.seek(0)
            return para

        payload = {}
        payload['total_time'] = timedelta()
        payload['words_read'] = 0

        para = get_para()
        no_words = len(para.split())

        para_message = await message.channel.send(para)
        start_time = datetime.now()

        async def on_respond(ctx, payload):
            message = ctx['message']

            nonlocal no_words, start_time

            if message.content == 'stop':
                await message.channel.send('note: last para not counted')
                await message.channel.send(interpret(payload, user.mention))
                return

            if message.content != 'ok':
                await message.reply('unexpected response.. stopped reading')
                await message.channel.send(interpret(payload, user))
                return

            payload['total_time'] += datetime.now() - start_time
            payload['words_read'] += no_words

            para = get_para()
            no_words = len(para.split())

            para_message = await message.channel.send(para)
            time_start = datetime.now()

            expires_at = datetime.now() + timedelta(seconds=30)
            timeout_ctx['message'] = para_message

            bot.add_message_session(expires_at, target, on_respond, 
                    timeout, timeout_ctx, payload)

        expires_at = datetime.now() + timedelta(seconds=30)
        timeout_ctx['message'] = para_message

        bot.add_message_session(expires_at, target, on_respond,
                timeout, timeout_ctx, payload)


    expires_at = datetime.now() + timedelta(seconds=10)
    target = {
        'author': user,
        'channel': message.channel
    }
    timeout_ctx = {
        'message': instructions_message,
        'bot': bot
    }

    bot.add_message_session(expires_at, target, on_ready,
            timeout, timeout_ctx, payload=False)

    def interpret(data, user):
        if data['words_read'] == 0:
            return f"no data to calculate {user}'s reading speed"

        reading_speed = data['total_time']/data['words_read']
        wpm = 60*(1/reading_speed.total_seconds())
        return f"{user}'s reading_speed: {wpm} words per minute"
