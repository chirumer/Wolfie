#### exports

message_listeners = []
    # list of all message listeners


#### main

def make_listener(type, listener):

    if type == 'message':
        message_listeners.append(listener)


#### message listeners

    # thanks listener
import src.bot_listeners.statistics.on_thanks as thanks
make_listener('message', thanks.listener)
