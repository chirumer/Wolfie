meta = {}
meta['invoking_keywords'] = ['hi']
meta['name'] = 'hi'
meta['description'] = 'bot says hi'

async def command(ctx, action):
    message = ctx['message']
    await message.reply('hi')
