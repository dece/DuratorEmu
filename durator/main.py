import durator.auth.login_server as login_server


def main():
    print("DuratorEmu - WoW 1.1.2.4125 Sandbox Server - Shgck 2015")
    my_login_server = login_server.LoginServer()
    my_login_server.start()


if __name__ == "__main__":
    main()
