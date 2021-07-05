import os
    # os related stuff
from dotenv import load_dotenv
    # loading env variables from env file

load_dotenv()
    # load env variables from env file


from src.bot import wolfie_bot
print('connecting bot')
wolfie_bot.run(os.getenv('bot_token'))
