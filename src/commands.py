commands = []

# decorator to add command to list
def command(func):
    commands.append({
        'command_name': func.__name__,
        'callback': func
    })

@command
async def hi(ctx, action):
    await ctx.reply('hi')
