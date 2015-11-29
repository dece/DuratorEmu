""" Utils for network comms. """


def netstr_to_str(netstr, encoding = "ascii"):
    """ Reverse those inverted bytes """
    return netstr.decode(encoding).strip("\x00")[::-1]
