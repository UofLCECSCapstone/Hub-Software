#################################################
# Database.py: Provides functions for           #
# accessing/interacting with the hub's database #
#################################################

import sqlite3

DATABASE_FILE = "hub-controller-db.db"


def get_connection():
    """
    Returns a SQLite connection to the
    hub controller's primary database.
    """
    connection = None

    try:
        connection = sqlite3.connect(DATABASE_FILE)
    except Exception:
        print(Exception)
        # TODO What types of exceptions should I handle? How should I handle them?
        raise NotImplementedError("TODO Errors here should be handled appropriately.")
        
    return connection
