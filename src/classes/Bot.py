#### imports

import discord
    # discord API-wrapper library


from src.classes.Emitter import Emitter
    # emits events, calls listeners

from src.classes.Session import Session
    # create session, inform sessions


#### class definition

class Bot(discord.Client):
        # discord bot interface

    # constructor
    def __init__(self, bot_prefix):
        discord.Client.__init__(
            self,
            activity = discord.Game(
                f'{bot_prefix} help'
            ) # default activity
        )
        self.bot_prefix = bot_prefix
            # bot commands prefix
        self._command = Emitter()
            # command handler
        self._event_emitter = Emitter()
            # event emitter
        self._sessions = Session()
            # sessions handler

    # add bot commands
    def add_commands(self, commands):
        
        # add listener for command and its aliases
        for command in commands:

            # add listener for command
            self._command.add_listener(
                command['name'],
                command['caller']
            )

            # add listeners for its aliases
            for alias in command['aliases']:
                self._command.add_listener(
                    alias,
                    command['caller']
                )

    # add message listeners
    def add_message_listeners(self, listeners):

        # add all listeners
        for listener in listeners:
            self._event_emitter.add_listener('message', listener)

    # on connection establishment
    async def on_ready(self):
        print('bot connected')

    # react to emoji add (cached messages only)
    async def on_reaction_add(self, reaction, user):

        # construct payload for informing sessions
        payload = {
            'reaction': reaction
        }
        # construct incoming for informing sessions
        incoming = {
            'user': user.id,
            'message': reaction.message.id,
            'emoji': reaction.emoji
        }
        # inform sessions
        in_session = await self._sessions.inform(
            'reaction', 
            incoming, 
            payload
        )

    # react to message
    async def on_message(self, message):

        #### helper functions

        help_str = (
            f'**type** {self.bot_prefix} help\n'
            'for help'
        )

        def is_instruction(text):
                # checks if text starts with bot prefix
            return(
                text.split() and
                text.split()[0] == self.bot_prefix
            )

        async def command_not_found():
                # notifies user: invalid command
            await message.reply(
                'no such command..\n'
                + help_str
            )

        async def no_command_specified():
                # notifies user: command not specified
            await message.reply(
                'no command specified..\n'
                + help_str
            )


        #### main

        # ignore bots
        if message.author.bot:
            return

        # construct payload for informing sessions
        payload = {
            'message': message,
        }
        # construct incoming for informing sessions
        incoming = {
            'user': message.author.id,
            'channel': message.channel.id
        }
        # inform sessions
        in_session = await self._sessions.inform(
            'message', 
            incoming, 
            payload
        )
            # in_session: whether it was handled by a session

        # if message is an instruction
        is_command = (
            is_instruction(message.content)
        )

        # if message is an instruction and not in session
        if is_command and not in_session:

            # user's instruction
            instruction = (
                message.content[len(self.bot_prefix):].strip()
            )

            # no instruction given
            if not instruction:
                await no_command_specified()
                return

            command = instruction.split()[0]
            action = instruction[len(command):].strip()

            # construct context for command listener
            ctx = {
                'action': action,
                'message': message,
                'bot': self
            }

            # try to execute the command
            is_handled = (
                self._command.emit(command, ctx)
            )

            # invalid command
            if not is_handled:
                await command_not_found()

        # construct payload for message listeners
        payload = {
            'message': message,
            'bot': self,
            'in_session': in_session,
            'is_command': is_command
        }
        # emit for message listeners
        self._event_emitter.emit('message', payload)

    # add emoji session
    async def add_emoji_session(self, timeout, targets,
                                    caller, timeout_caller):
        await self._sessions.add(
            'reaction', timeout, targets,
            caller, timeout_caller
        )

    # add message session
    async def add_message_session(self, timeout, targets,
                                    caller, timeout_caller):
        await self._sessions.add(
            'message', timeout, targets,
            caller, timeout_caller
        )
