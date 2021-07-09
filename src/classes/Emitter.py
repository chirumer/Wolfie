#### imports

import asyncio
    # for asynchronous programming

from inspect import signature
    # for inspecting function signature


#### class definition

class Emitter:
        # emits events
        # calls event listeners

    _next_id = 0
        # id of the next listener

    # constructor
    def __init__(self):
        self._events = {}
            # maps events to their listeners

    # add a listener
    def add_listener(self, event, caller):

        # get listener id
        listener_id = self._next_id
        self._next_id += 1

        # construct the listener
        listener = {
            'id': listener_id,
            'caller': caller
        }

        # add our listener
        if event in self._events:
            self._events[event].append(listener)
        else:
            self._events[event] = [listener]

        listener_identity = {
            'event': event,
            'id': listener_id
        }
        return listener_identity

    # emit event to listeners
    def emit(self, event, payload = None):

        if not event in self._events:
                # no listeners for the event
            return False 
            # False (no listeners)

        # call listeners
        for listener in self._events[event]:

            asyncio.create_task(
                listener['caller']()
                if 
                len(signature(listener['caller']).parameters) == 0
                else
                listener['caller'](payload)
            )

        return True
        # True (found listener)

    # remove an event listener
    def remove_listener(self, listener_identity):
        event = listener_identity['event']
        remove_id = listener_identity['id']

        if event not in self._events:
                # no listeners for event
            return

        if len(self._events[event]) <= 1:
                # if only one listener under event
            self._events.pop(event)
            return

        self._events[event] = [
            listener
            for listener in self._events[event]
            if listener['id'] != remove_id
        ]

    # remove all listeners for an event
    def remove_all_listeners(self, event):
        self._events.pop(event)
