""" Misc utils """

import binascii
import string


def hexlify(data):
    """ Short handle to get data as a readable string. """
    return binascii.hexlify(data).decode("ascii")

def dump_data(data):
    """ Pretty print binary data in a Hexdump fashion. """
    dump = ""
    index = 0
    while index < len(data):
        data_slice = data[ index : index+16 ]
        offset_str = _get_offset_string(index)
        data_str = _get_hexdump_string(data_slice)
        ascii_str = _get_asciidump_string(data_slice)
        dump += "{} {:<47} {}\n".format(offset_str, data_str, ascii_str)
        index += 16
    return dump

def _get_offset_string(index):
    offset = hex(index)[2:]
    offset = offset.zfill(8)
    return offset

def _get_hexdump_string(data):
    hexdump = binascii.hexlify(data).decode("ascii")
    spaced_hexdump = ""
    index = 0
    while index < len(hexdump):
        spaced_hexdump += hexdump[ index : index+2 ] + " "
        index += 2
    return spaced_hexdump.strip()

def _get_asciidump_string(data):
    asciidump = ""
    for char in data:
        char = chr(char)
        if char in string.printable and not char in "\r\n\t":
            asciidump += char
        else:
            asciidump += "."
    return asciidump
