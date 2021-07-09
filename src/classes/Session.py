#### imports

import asyncio
    # for asynchronous programming

from inspect import signature
    # for inspecting function signature


#### class definition

class Session:
        # adds sessions
        # informs sessions

    # constructor
    def __init__(self):
        self._types = {}
            # maps types to their sessions
        self._lock = asyncio.Lock()
            # for preventing race conditions

    # add a session
    async def add(self, type, timeout, targets, caller, timeout_caller):

        #### helper functions

        # add session to list
        async def add_session():

            # lock to prevent race condition
            async with self._lock:
                if type in self._types:
                    self._types[type].append(session)
                else:
                    self._types[type] = [session]

        # timeout the session
        async def expire_session():

            # wait until timeout
            await asyncio.sleep(timeout)

            # lock to prevent race condition
            async with self._lock:

                # remove session
                for index, sess in enumerate(self._types.get(type, [])):
                    if sess == session:
                        asyncio.create_task(
                            timeout_caller()
                        )
                        self._types[type].pop(index)
                        if not self._types[type]: # is empty
                            self._types.pop(type)
                        break


        #### main

        if not isinstance(targets, list):
            targets = [targets]

        session = {
            'targets': targets,
            'caller': caller
        }

        # add session to sessions
        await add_session()

        # add timeout watcher
        asyncio.create_task(expire_session())

    # inform sessions of an event
    async def inform(self, type, incoming, payload = None):

        #### helper functions

        async def inform_sessions():

            # lock to prevent race conditions
            async with self._lock:

                for index, session in enumerate(self._types[type]):
                    if incoming in session['targets']:
                        asyncio.create_task(
                            session['caller']()
                            if 
                            len(signature(session['caller']).parameters) == 0
                            else
                            session['caller'](payload)
                        )
                        self._types[type].pop(index)
                        if not self._types[type]: # is empty
                            self._types.pop(type)
                        in_session = True
                        # True (incoming was in a session)


        #### main

        if not type in self._types:
                # no sessions for type
            return False
            # False: (incoming was not in any session)

        # inform sessions
        return await inform_sessions()
            # returns whether incoming was in sessions
