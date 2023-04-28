from code_map import code_maps
import re


shift_jis = "shift-jis"


class Decoder:
    def __init__(self, character_encoding_file):
        self.character_encoding = read_character_encoding(filename=character_encoding_file)

    def decode(self, character_bytes):
        if character_bytes < b'\x88\x9f':
            raise ValueError('Unexpected bytes ' + character_bytes)
        if character_bytes > b'\x9b\xff':
            raise ValueError('Unexpected bytes ' + character_bytes)

        for start, end, loc in code_maps:
            if start <= character_bytes < end:
                position = loc + subtract_bytes(character_bytes, start)
                return self.character_encoding[position]

    def read_script(self, line: bytes):
        decoded_string = ""
        i = 0
        while i < len(line):
            if line[i:i + 1] < b'\x80':
                character_byte = line[i:i + 1]
                character = character_byte.decode(encoding=shift_jis, errors='strict')
                decoded_string = decoded_string + character
                i = i + 1
            else:
                character_bytes = line[i:i + 2]
                if b'\x88\x9f' <= character_bytes <= b'\xea\xa0':
                    decoded_character = self.decode(character_bytes)
                    decoded_string = decoded_string + decoded_character
                else:
                    character = character_bytes.decode(encoding=shift_jis, errors='strict')
                    decoded_string = decoded_string + character
                i = i + 2
        return decoded_string

    def read_script_from_file(self, filename: str):
        with open(filename, mode='rb') as f:
            return self.read_script(f.read())

    def encode(self, character):
        index = self.character_encoding.index(character)
        for start, end, loc in reversed(code_maps):
            if loc <= index:
                return add_bytes(start, int_to_bytes(index - loc))

    def write_script(self, script: str):
        script_bytes = b''
        for character in script:
            if character in self.character_encoding:
                character_byte = self.encode(character)
                script_bytes = script_bytes + character_byte
            else:
                character_byte = character.encode(encoding=shift_jis, errors='strict')
                script_bytes = script_bytes + character_byte
        return script_bytes

    def write_script_to_file(self, filename: str, script: str):
        with open(filename, mode='wb') as f:
            f.write(self.write_script(script))


def read_character_encoding(filename='res/wa2.cht.txt'):
    with open(filename, 'r', encoding='utf-8') as file:
        return re.sub(r"\s", "", file.read(), flags=re.UNICODE)


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
