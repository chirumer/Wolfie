#### imports

import os
    # for os related stuff


#### main

def get_database(db_name, connection_string):
        # construct database object
    from pymongo import MongoClient
    client = MongoClient(connection_string)
    return client[db_name]

_db = get_database(
    'Wolfie-bot',
    os.getenv('db_string')
)


#### exports

howls_db = _db['howls']
thanks_db = _db['thanks']
