from peewee import MySQLDatabase


_USER = "durator"
_PASS = "durator"

DB = MySQLDatabase("durator", user = _USER, password = _PASS)


def db_connection(func):
    """ Decorator that connects to the db with correct credentials and properly
    closes the connection after return. """
    def decorator(*args, **kwargs):
        DB.connect()
        return_value = func(*args, **kwargs)
        DB.close()
        return return_value
    return decorator
