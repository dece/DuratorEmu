#!/usr/bin/env python3

import argparse

from durator.auth.login_server import LoginServer
from durator.world.world_server import WorldServer
from pyshgck.logger import LOG


def main():
    LOG.info("DuratorEmu - WoW 1.1.2.4125 Sandbox Server - Shgck 2015")

    argparser = argparse.ArgumentParser()
    argparser.add_argument("server_type", type = str, help = "server type")
    args = argparser.parse_args()

    if args.server_type == "login":
        login_server = LoginServer()
        login_server.start()
    elif args.server_type == "world":
        world_server = WorldServer()
        world_server.start()


if __name__ == "__main__":
    main()
