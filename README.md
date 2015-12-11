DuratorEmu
==========

World of Warcraft 1.1.2.4125 tiny emulator.

Dependencies:

* Python 3.4
* MySQL (anything slightly recent should be fine)
* Peewee (available in PyPI)
* A Python MySQL driver (PyMySQL preferably, or MySQLdb)
* PyShgck (available on this Gitlab).

Quick MySQL database setup:

* CREATE DATABASE durator;
* CREATE USER 'durator'@'%' IDENTIFIED BY 'durator'
* GRANT ALL PRIVILEGES ON durator.* TO 'durator'@'%' IDENTIFIED BY 'durator';

Feel free to use other credentials (but update the database code configuration),
and to narrow the hostname to something more private than a full wildcard.
