""" Colored logger (http://stackoverflow.com/a/1336640) """

import ctypes
import logging
import platform


_FORMAT      = "%(asctime)s %(levelname)-8s %(message)s"
_DATE_FORMAT = "%H:%M:%S"
_LOG_LEVEL   = logging.DEBUG

_STD_INPUT_HANDLE     = -10
_STD_OUTPUT_HANDLE    = -11
_STD_ERROR_HANDLE     = -12

_FOREGROUND_BLACK     = 0x0000
_FOREGROUND_BLUE      = 0x0001
_FOREGROUND_GREEN     = 0x0002
_FOREGROUND_CYAN      = 0x0003
_FOREGROUND_RED       = 0x0004
_FOREGROUND_MAGENTA   = 0x0005
_FOREGROUND_YELLOW    = 0x0006
_FOREGROUND_GREY      = 0x0007
_FOREGROUND_INTENSITY = 0x0008
_FOREGROUND_WHITE     = _FOREGROUND_BLUE | _FOREGROUND_GREEN | _FOREGROUND_RED

_BACKGROUND_BLACK     = 0x0000
_BACKGROUND_BLUE      = 0x0010
_BACKGROUND_GREEN     = 0x0020
_BACKGROUND_CYAN      = 0x0030
_BACKGROUND_RED       = 0x0040
_BACKGROUND_MAGENTA   = 0x0050
_BACKGROUND_YELLOW    = 0x0060
_BACKGROUND_GREY      = 0x0070
_BACKGROUND_INTENSITY = 0x0080


def _add_coloring_to_emit_windows(func):

    def _out_handle(self):
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
    out_handle = property(_out_handle)

    def _set_color(self, code):
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    def new(*args):
        levelno = args[1].levelno
        if levelno >= 50:
            color = _FOREGROUND_RED | _FOREGROUND_INTENSITY
        elif levelno >= 40:
            color = _FOREGROUND_RED | _FOREGROUND_INTENSITY
        elif levelno >= 30:
            color = _FOREGROUND_YELLOW | _FOREGROUND_INTENSITY
        elif levelno >= 20:
            color = _FOREGROUND_WHITE
        elif levelno >= 10:
            color = _FOREGROUND_CYAN
        else:
            color = _FOREGROUND_WHITE

        args[0]._set_color(color)
        ret = func(*args)
        args[0]._set_color(_FOREGROUND_WHITE)
        return ret
    return new

def _add_coloring_to_emit_ansi(func):

    black, red, green, yellow, blue, magenta, cyan, white = range(8)

    def new(*args):
        levelno = args[1].levelno
        if levelno >= 50:
            color = '\x1b[31m'
        elif levelno >= 40:
            color = '\x1b[31m'
        elif levelno >= 30:
            color = '\x1b[33m'
        elif levelno >= 20:
            color = '\x1b[37m'
        elif levelno >= 10:
            color = '\x1b[36m'
        else:
            color = '\x1b[0m'
        args[1].msg = color + args[1].msg +  '\x1b[0m'

        return func(*args)
    return new

def _get_logger():
    logging.basicConfig(level = _LOG_LEVEL, format = _FORMAT,
        datefmt = _DATE_FORMAT)
    logger = logging.getLogger()

    _patch_logging_stream_handler()

    return logger

def _patch_logging_stream_handler():
    if platform.system() == "Windows":
        coloring_func = _add_coloring_to_emit_windows
    else:
        coloring_func = _add_coloring_to_emit_ansi
    logging.StreamHandler.emit = coloring_func(logging.StreamHandler.emit)


LOG = _get_logger()
