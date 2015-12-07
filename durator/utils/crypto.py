import hashlib


def sha1(data):
    hasher = hashlib.sha1(data)
    return hasher.digest()

def sha1_interleave(big_int):
    big_array = int.to_bytes(big_int, 128, "little")
    big_array = big_array.rstrip(b"\x00")
    if len(big_array) % 2 == 1:
        big_array = big_array[1:]

    part1 = b""
    part2 = b""
    for i in range(len(big_array)):
        if i % 2 == 0:
            part1 += big_array[i:i+1]
        else:
            part2 += big_array[i:i+1]

    hash1 = sha1(part1)
    hash2 = sha1(part2)
    interleaved = b""
    for i in range(20):
        interleaved += hash1[i:i+1] + hash2[i:i+1]

    return interleaved
