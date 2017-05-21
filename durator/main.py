#!/usr/bin/env python3

import argparse

from durator.auth.login_server import LoginServer
from durator.db.database_client import DatabaseClient
from durator.world.world_server import WorldServer
from durator.common.log import LOG


MODULES = {
    "login": LoginServer,
    "world": WorldServer,
    "db": DatabaseClient
}


def main():
    LOG.info("DuratorEmu - WoW 1.1.2.4125 Sandbox Server - Shgck 2016")

    argparser = argparse.ArgumentParser()
    argparser.add_argument("module", type = str, help = "module to start")
    args = argparser.parse_args()

    if args.module in MODULES:
        module_class = MODULES[args.module]
        module = module_class()
        module.start()
    else:
        print("Unknown module:", args.module)


if __name__ == "__main__":
    main()
