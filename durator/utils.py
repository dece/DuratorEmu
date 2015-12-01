import binascii


def hexlify(data):
    return binascii.hexlify(data).decode("ascii")
