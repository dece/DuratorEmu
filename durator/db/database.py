from peewee import MySQLDatabase, OperationalError

from durator.config import CONFIG
from pyshgck.logger import LOG


_DB_NAME = CONFIG["db"]["db_name"]
_DB_USER = CONFIG["db"]["db_user"]
_DB_PASS = CONFIG["db"]["db_pass"]

DB = MySQLDatabase(_DB_NAME, user = _DB_USER, password = _DB_PASS)


# Count the number of functions currently using the db_connection decorator, to
# avoid closing the connection in a callee when the caller will try to close it
# as well.
_NUM_CONNECTIONS = 0


def db_connection(func):
    """ Decorator that connects to the db with correct credentials and properly
    closes the connection after return. If a connection couldn't be made, it
    returns None and does not call the decorated function. """

    def decorator(*args, **kwargs):
        global _NUM_CONNECTIONS
        assert _NUM_CONNECTIONS >= 0

        _NUM_CONNECTIONS += 1
        if _NUM_CONNECTIONS == 1:
            try:
                DB.connect()
            except OperationalError as exc:
                LOG.error("A problem occured while accessing the database!")
                LOG.error("Is the MySQL server started?")
                LOG.error("Is the Durator user created? (see database creds)")
                LOG.error("Does it have full access to the durator database?")
                LOG.error(str(exc))
                _NUM_CONNECTIONS -= 1
                return None

        return_value = func(*args, **kwargs)

        _NUM_CONNECTIONS -= 1
        if _NUM_CONNECTIONS == 0:
            try:
                DB.close()
            except OperationalError as exc:
                LOG.error("Couldn't disconnect from the database: " + str(exc))

        return return_value

    return decorator
