from configparser import ConfigParser
from os.path import dirname, join, normpath


ROOT_DIR = normpath(join(dirname(__file__), "../"))
CONFIG_DIR = join(ROOT_DIR, "config")
DURATOR_CONFIG = join(CONFIG_DIR, "durator.ini")

ALL_CONFIG_FILES = [DURATOR_CONFIG]

def _load_config():
    global CONFIG
    CONFIG = ConfigParser()
    CONFIG.read(ALL_CONFIG_FILES)


# Static config object, loaded when the module is imported.
CONFIG = None


_load_config()
