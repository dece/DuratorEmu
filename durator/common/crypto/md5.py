import hashlib


def md5(data):
    """ Return the MD5 of bytes data, as bytes. """
    hasher = hashlib.md5(data)
    return hasher.digest()
