#!/usr/bin/env python3

import argparse

import durator.auth.login_server as login_server
from pyshgck.logger import LOG


def main():
    LOG.info("DuratorEmu - WoW 1.1.2.4125 Sandbox Server - Shgck 2015")

    argparser = argparse.ArgumentParser()
    argparser.add_argument("server", type = str, help = "server type")
    args = argparser.parse_args()

    if args.server_type == "login":
        my_login_server = login_server.LoginServer()
        my_login_server.start()
    elif args.server_type == "world":
        pass


if __name__ == "__main__":
    main()
