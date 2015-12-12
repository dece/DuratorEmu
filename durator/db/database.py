from peewee import MySQLDatabase


_USER = "durator"
_PASS = "durator"

DB = MySQLDatabase("durator", user = _USER, password = _PASS)


# Count the number of functions currently using the db_connection decorator, to
# avoid closing the connection in a callee when the caller will try to close it
# as well.
_NUM_CONNECTIONS = 0


def db_connection(func):
    """ Decorator that connects to the db with correct credentials and properly
    closes the connection after return. """
    def decorator(*args, **kwargs):
        global _NUM_CONNECTIONS
        assert _NUM_CONNECTIONS >= 0

        _NUM_CONNECTIONS += 1
        if _NUM_CONNECTIONS == 1:
            DB.connect()

        return_value = func(*args, **kwargs)

        _NUM_CONNECTIONS -= 1
        if _NUM_CONNECTIONS == 0:
            DB.close()
        return return_value
    return decorator
