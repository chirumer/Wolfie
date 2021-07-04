from os import getenv
    # reading env variables
from dotenv import load_dotenv
    # loading env variables from env file
import discord
    # discord API wrapper
import json
    # parse json file
import asyncio
    # asynchronous programming
from datetime import datetime
    # working with time

load_dotenv()
    # load env variables from env file

config = json.load(open('../config.json'))
    # load config


class Event_dispatcher():
        # dispatch events to listeners

    _next_listener_id = 0
        # id of next event listener

    # constructor 
    def __init__(self):
        self._listeners = {}
            # maps event-type to listeners

    # add listener
    def add_listener(self, event_type, callback):

        # map event to its listeners
        listener_id = self._next_listener_id
        self._next_listener_id += 1
        if event_type not in self._listeners:
            self._listeners[event_type] = [{
                'id': listener_id,
                'callback': callback
            }]
        else:
            self._listeners.get(event_type).append({
                'id': listener_id,
                'callback': callback
            })
        return listener_id
            # unique id

    # remove event listener
    def remove_listener(self, event_type, remove_id):

        for index, listener in enumerate(self._listeners.get(event_type)):
            if listener['id'] == remove_id:
                self._listeners.get(event_type).pop(index)
                break
        if not self._listeners.get(even_type):
                # no listeners for event
            self._listeners.pop(event_type)

    # remove all listeners
    def remove_all_listeners(self, event_type):
        self._listeners.pop(event_type)

    # dispatch event to its listeners
    def emit(self, event_type, payload):
        if not self._listeners.get(event_type):
                # no listeners
            return
        for listener in self._listeners.get(event_type):
            asyncio.create_task(
                listener['callback'](payload)
            )


class Command_handler():
    # handles command events

    _next_listener_id = 0
        # id of the next listener

    # constructor
    def __init__(self):
        self._listeners = {}
            # maps command to its listeners
        self._default_listeners = []
            # maps command to default listeners

    # add listener
    def add_listener(self, command, callback):

        # map command to array of listeners
        listener_id = self._next_listener_id
        self._next_listener_id += 1
        if command not in self._listeners:
            self._listeners[command] = [{
                    'id': listener_id,
                    'callback': callback
            }]
        else:
            self._listeners.get(command).append({
                'id': listener_id,
                'callback': callback
            })

        return listener_id 
            # unique id

    # add default listener
    def add_default_listener(self, callback):

        listener_id = self._next_listener_id
        self._next_listener_id += 1

        # add default listeners
        self._default_listeners.append({
            'id': listener_id,
            'callback': callback
        })

        return listener_id
                
    # remove listener
    def remove_listener(self, command, remove_id):

        for index, listeners in enumerate(self._listeners.get(command)):
            if listeners['id'] == remove_id:
                self._listeners.get(command).pop(index)
                break
        if not self._listeners.get(command):
                # no listeners for command
            self._listeners.pop(command)

    def remove_default_listener(self, remove_id):

        for index, listener in enumerate(self._default_listeners):
            if listener['id'] == remove_id:
                self._default_listeners.pop(index)
                break
        
    # remove all listeners for command
    def remove_all_listeners(self, command):
        self._listeners.pop(command)

    # remove all default listeners
    def remove_all_default_listeners(self):
        self._default_listeners = []

    # call listeners
    def emit(self, command, ctx, action):
        if not self._listeners.get(command):
                # no listeners for the command, 
                # call default listeners
            for listener in self._default_listeners:
                asyncio.create_task(
                    listener['callback'](ctx)
                )
            return

        # run all listeners asynchronously
        for listener in self._listeners.get(command):
            asyncio.create_task(
                listener['callback'](ctx, action)
            )


class Message_sessions_handler():
        # handles message sessions

    # constructor
    def __init__(self):
        self._sessions = []

    # add a session
    def add(self, expires_at, target, callback, timeout_callback, 
            timeout_ctx, payload):

        self._sessions.append({
            'expires_at': expires_at,
            'target': target,
            'callback': callback,
            'timeout_callback': timeout_callbacklen,
            'timeout_ctx': timeout_ctx,
            'payload': payload
        })

    # check if part of session
    def emit(self, incoming, ctx):

        any_expired = False
        is_part_of_session = False
        time_now = datetime.now()

        for index, session in enumerate(self._sessions):
            if session['expires_at'] <= time_now:
                any_expired = True
            if session['target'] == incoming:
                asyncio.create_task(
                        session['callback'](ctx, session['payload'])
                )
                self._sessions.pop(index)
                is_part_of_session = True
                break

        if any_expired:
                # remove expired sessions
            new_sessions = []
            for session in self._sessions:
                if session['expires_at'] > time_now:
                    new_sessions.append(session)
                else:
                    asyncio.create_task(
                        session['timeout_callback'](
                            session['timeout_ctx'],
                            session['payload']
                        )
                    )
            self._sessions = new_sessions

        return is_part_of_session


class Bot(discord.Client):

    def __init__(self, bot_prefix):
        discord.Client.__init__(self)
        self.bot_prefix = bot_prefix
        self._command_handler = Command_handler()
        self._event_handler = Event_dispatcher()
        self._message_sessions = Message_sessions_handler()

    # add commands
    def add_commands(self, commands):
        for command in commands:
            self._command_handler.add_listener(
                command['command_name'],
                command['callback']
            )

    # add message session
    def add_message_session(self, expires_at, target, callback, timeout_callback,
            timeout_ctx, payload):
        self._message_sessions.add(expires_at, target, callback, timeout_callback,
                timeout_ctx, payload)

    # add default command
    def add_default_command(self, default_command):
        self._command_handler.add_default_listener(default_command)


    # add message listener
    def add_message_listener(self, callback):
        self._event_handler.add_listener('message', callback)

    # notify that we've connected
    async def on_ready(self):
        print('Logged on as', self.user)


    async def on_message(self, message):
        
        # check if message part of sessions
        incoming = {
            'author': message.author,
            'channel': message.channel
        }
        ctx = {
            'message': message,
            'bot': self
        }
        in_session = self._message_sessions.emit(incoming, ctx)

        # dispatch message event
        payload = {}
        payload['message'] = message
        payload['is_self'] = message.author == self.user
        payload['in_session'] = in_session
        self._event_handler.emit('message', payload)

        # don't respond to ourselves
        if message.author == self.user:
            return

        # ignore session messages
        if in_session:
            return

        # if user is instructing us
        if message.content.startswith(self.bot_prefix):

            command = (
                message.content[len(self.bot_prefix):].split()
                    and message.content[len(self.bot_prefix):].split()[0]
            )

            if not command:

                # incomplete command
                await message.reply(
                    'No command specified..\n'
                    f"**type** {self.bot_prefix} help\n"
                    'for help'
                )
            else:
                ctx = {}
                ctx['message'] = message
                ctx['bot'] = self
                action = message.content[len(self.bot_prefix):].strip()
                self._command_handler.emit(command, ctx, action)


wolfie_bot = Bot(config['bot_prefix'])
from commands import commands, default_command
wolfie_bot.add_commands(commands)
wolfie_bot.add_default_command(default_command)
from statistics import guild_message_statistics
wolfie_bot.add_message_listener(guild_message_statistics)
print('connecting bot')
wolfie_bot.run(getenv('bot_token'))
