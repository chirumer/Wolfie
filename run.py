#### imports

import os
    # for os stuff
from dotenv import load_dotenv
    # to load env variables from file


#### main

# load env variables
load_dotenv()

if __name__ == '__main__':
        # if being run as a script

    from src.main import wolfie_bot


    # start wolfie discord bot
    print('connecting bot')
    wolfie_bot.run(os.getenv('bot_token'))
