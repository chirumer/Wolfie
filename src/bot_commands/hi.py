meta = {}
meta['invoking_keywords'] = ['hi']
meta['name'] = 'hi'
meta['description'] = 'wolie says hi'

async def command(ctx, action):
    message = ctx['message']
    await message.reply('*growls*')
