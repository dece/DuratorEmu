import threading

from peewee import MySQLDatabase, OperationalError

from durator.config import CONFIG, DEBUG
from pyshgck.logger import LOG


_DB_NAME = CONFIG["db"]["db_name"]
_DB_USER = CONFIG["db"]["db_user"]
_DB_PASS = CONFIG["db"]["db_pass"]

DB = MySQLDatabase(_DB_NAME, user = _DB_USER, password = _DB_PASS)


class _DbConnector(object):
    """ Internal component that handle threaded access to the database.

    The db_connection decorator needs to keep count of the number of functions
    currently accessing the database, to avoid closing the connection in a
    callee when the caller will try to close it as well, or when several
    connections need a database access at the same time.

    The count can be accessed safely thanks to the associated lock. This lock
    must NOT be acquired for the db requests but only for the connection
    counter. This is MySQL, we should be able to send threaded stuff without
    issues, we just need to keep the gates.
    """

    def __init__(self, database):
        self.database = database
        self.num_connections = 0
        self.num_connections_lock = threading.Lock()

    def connect(self):
        """ Connect to the database, return True on success. """
        with self.num_connections_lock:
            assert self.num_connections >= 0
            self.num_connections += 1
            if self.num_connections == 1:
                try:
                    self.database.connect()
                    if DEBUG:
                        LOG.debug("[db] Database connected")
                except OperationalError as exc:
                    _DbConnector.log_error("connect", exc)
                    self.num_connections -= 1
                    return False
        return True

    def close(self):
        """ Close the database connection, return True on success. """
        with self.num_connections_lock:
            self.num_connections -= 1
            if self.num_connections == 0:
                try:
                    self.database.close()
                    if DEBUG:
                        LOG.debug("[db] Database closed")
                except OperationalError as exc:
                    _DbConnector.log_error("close", exc)
                    return False
        return True

    @staticmethod
    def log_error(operation, exception):
        LOG.error("A problem occured during operation '{}'".format(operation))
        LOG.error("Is the MySQL server started?")
        LOG.error("Is the Durator user created? (see database creds)")
        LOG.error("Does it have full access to the durator database?")
        LOG.error(str(exception))


_DB_CONNECTOR = _DbConnector(DB)


def db_connection(func):
    """ Decorator that connects to the db with correct credentials and properly
    closes the connection after return.

    If a connection couldn't be made, it returns None and does not call the
    decorated function. However, if a connection couldn't be closed, we still go
    on and return the function return value and assume it isn't that bad.
    """

    def db_connection_decorator(*args, **kwargs):
        if not _DB_CONNECTOR.connect():
            return None

        return_value = None
        try:
            return_value = func(*args, **kwargs)
        finally:
            _DB_CONNECTOR.close()
        return return_value

    return db_connection_decorator
