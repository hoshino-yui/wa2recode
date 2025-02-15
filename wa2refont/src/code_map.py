code_maps = [
    (b'\x88\x9f', b'\x88\xff', 0),
    (b'\x89\x40', b'\x89\xff', -95 + 189),
    (b'\x8a\x40', b'\x8a\xff', -95 + 189 * 2),
    (b'\x8b\x40', b'\x8b\xff', -95 + 189 * 3),
    (b'\x8c\x40', b'\x8c\xff', -95 + 189 * 4),
    (b'\x8d\x40', b'\x8d\xff', -95 + 189 * 5),
    (b'\x8e\x40', b'\x8e\xff', -95 + 189 * 6),
    (b'\x8f\x40', b'\x8f\xff', -95 + 189 * 7),
    (b'\x90\x40', b'\x90\xff', -95 + 189 * 8),
    (b'\x91\x40', b'\x91\xff', -95 + 189 * 9),
    (b'\x92\x40', b'\x92\xff', -95 + 189 * 10),
    (b'\x93\x40', b'\x93\xff', -95 + 189 * 11),
    (b'\x94\x40', b'\x94\xff', -95 + 189 * 12),
    (b'\x95\x40', b'\x95\xff', -95 + 189 * 13),
    (b'\x96\x40', b'\x96\xff', -95 + 189 * 14),
    (b'\x97\x40', b'\x97\xff', -95 + 189 * 15),
    (b'\x98\x40', b'\x98\x7f', -95 + 189 * 16),
    (b'\x98\x9f', b'\x98\xff', -95 + 51 + 189 * 16),
    (b'\x99\x40', b'\x99\xff', -95 + 51 + 94 + 189 * 16),
    (b'\x9a\x40', b'\x9a\xff', -95 + 51 + 94 + 189 * 17),
    (b'\x9b\x40', b'\x9b\xff', -95 + 51 + 94 + 189 * 18),
    (b'\x9c\x40', b'\x9c\xff', -95 + 51 + 94 + 189 * 19),
    # Omit remaining ones, unused for the purpose of this project.
]


def get_index_from_bytes(character_bytes):
    for start, end, loc in code_maps:
        if start <= character_bytes < end:
            return loc + subtract_bytes(character_bytes, start)

    raise ValueError('Unknown bytes ' + character_bytes)


def get_bytes_from_index(index):
    for start, end, loc in reversed(code_maps):
        if loc <= index:
            return add_bytes(start, int_to_bytes(index - loc))


def subtract_bytes(bytes1: bytes, bytes2: bytes):
    int1 = int.from_bytes(bytes1, byteorder='big')
    int2 = int.from_bytes(bytes2, byteorder='big')
    result = int1 - int2
    return result


def add_bytes(bytes1: bytes, bytes2: bytes):
    int1 = int.from_bytes(bytes1, byteorder='big')
    int2 = int.from_bytes(bytes2, byteorder='big')
    result = int1 + int2
    return int_to_bytes(result)


def int_to_bytes(int1):
    return int1.to_bytes(2, byteorder='big')
