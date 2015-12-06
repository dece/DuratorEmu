""" Utils for network comms. """


def netstr_to_str(netstr, encoding = "ascii"):
    """ Reverse those inverted bytes and return a string. """
    return netstr.decode(encoding).strip("\x00")[::-1]

def ip_to_str(ip_addr):
    """ Format an IPv4 tuple as string. """
    return "{}.{}.{}.{}".format(ip_addr[0], ip_addr[1], ip_addr[2], ip_addr[3])
