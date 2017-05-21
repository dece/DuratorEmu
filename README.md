DuratorEmu
==========

This is a World of Warcraft 1.1.2.4125 tiny server emulator, written in Python,
which tries to remain small, clean and understandable. The goal is to handle
several player and basic stuff like chat and groups to have some fun with old
school exploration techniques.

I'll repeat that again: it is a TINY emulator, which means that it is not meant
for serious use (you shouldn't run a serious private server anyway). There are
very few sanity checks beside basic auth, and almost nothing that a client
wouldn't do is checked for. It is also not meant to be an efficient
implementation. It is in Python, and nothing is done to circumvent the GIL. The
threaded connections use locks pretty much anywhere because I didn't want to do
a full-fledged concurrency system, and I'm not even implying that I could do
that correctly. It would mean that I have to look in my reading notes about the
readers-writers problems and stuff, and these notes are almost unreadable.

Use it to have fun exploring with a few friends, that's all.

Demo: https://youtu.be/uucpgeK3ILk



Installation
------------

Dependencies:

- Python 3.4+
- MySQL
- Peewee, the Python ORM used
- A Python MySQL driver
- PyShgck

### Python 3.4+

Get that from their website.

### MySQL

Get a community package from their website, anything slightly recent should be
fine. Once the MySQL server is running, you need to setup a database and an
account to access this database.

Quick MySQL database setup:

- CREATE DATABASE durator;
- CREATE USER 'durator'@'%' IDENTIFIED BY 'durator'
- GRANT ALL PRIVILEGES ON durator.* TO 'durator'@'%' IDENTIFIED BY 'durator';

Feel free to use other credentials (but update the database code configuration),
and to narrow the hostname to something more private than a full wildcard.

### Peewee

Available in PyPI:

``` bash
pip install peewee
```

### Python MySQL driver

You only need one of them, preferably PyMySQL because that's the one I use, but
both are available in PyPI:

``` bash
pip install pymysql
# OR
pip install mysqldb
```

### PyShgck

Grab this [tag](https://gitlab.com/Shgck/py-shgck-tools/tags/v1.1.0) and install
it with the setup batch file.



Configuration
-------------

Configure the database and create an account with the database client

``` bash
cd DuratorEmu
python3 -m durator.main db
# use the commands 'install' and 'account'
```

Then just use `start.bat`, or manually start the login and world servers in
different consoles:

``` bash
python3 -m durator.main login
python3 -m durator.main world
```



Documentation
-------------

Some related projects and documentation that I used, first for Vanilla (mostly
1.12):

- [WoWCore](https://github.com/RomanRom2/WoWCore/)
- [MangosClassic](https://github.com/cmangos/mangos-classic)
- [Ember](https://github.com/EmberEmu/Ember)
- [Miceiken's server](http://git.clusterbrain.net/miceiken/WoWClassicServer)

More recent but still interesting sources:

- [Mangos wiki](https://getmangos.eu/wiki/Reference%20Information)
- [ArcEmu wiki](http://www.arcemu.org/wiki/Packets)

Also, thanks to #modcraft for being nice folks :]
