from configparser import ConfigParser
import os


# TODO is there a way to get the root directory from which the whole project is
# started? without __file__ etc
ROOT_DIR = os.path.abspath("../../../")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
DURATOR_CONFIG = os.path.join(CONFIG_DIR, "durator.ini")

ALL_CONFIG_FILES = [DURATOR_CONFIG]


def _load_config():
    global CONFIG
    CONFIG = ConfigParser()
    CONFIG.read(ALL_CONFIG_FILES)


# Static config object, loaded when the module is imported.
CONFIG = None


_load_config()
