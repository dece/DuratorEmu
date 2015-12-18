DuratorEmu
==========

World of Warcraft 1.1.2.4125 tiny emulator.



Installation
------------

Dependencies:

- Python 3.4
- MySQL, anything slightly recent should be fine
- Peewee, the Python ORM used, available in PyPI
- A Python MySQL driver, PyMySQL preferably (in PyPI), or maybe MySQLdb
- PyShgck, a toolbox available on this Gitlab.

Quick MySQL database setup:

- CREATE DATABASE durator;
- CREATE USER 'durator'@'%' IDENTIFIED BY 'durator'
- GRANT ALL PRIVILEGES ON durator.* TO 'durator'@'%' IDENTIFIED BY 'durator';

Feel free to use other credentials (but update the database code configuration),
and to narrow the hostname to something more private than a full wildcard.

Configure the database and create an account with the database client

``` bash
cd DuratorEmu
python3 -m durator.main db
```

Then just start the login and world servers in different consoles.

``` bash
python3 -m durator.main login
python3 -m durator.main world
```



Documentation
-------------

Some related projects and documentation that I used, first for Vanilla (mostly
1.12):

- [MangosClassic](https://github.com/cmangos/mangos-classic)
- [Ember](https://github.com/EmberEmu/Ember)
- [Miceiken's server](http://git.clusterbrain.net/miceiken/WoWClassicServer)

More recent but still interesting sources:

- [Mangos wiki](https://getmangos.eu/wiki/Reference%20Information)
- [ArcEmu wiki](http://www.arcemu.org/wiki/Packets)

Also, thanks to #modcraft for being nice folks :]
