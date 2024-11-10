import utils
from code_map import code_maps
from os import makedirs
from os.path import join


class Decoder:
    def __init__(self, character_encoding_file):
        self.character_encoding = utils.read_character_encoding(filename=character_encoding_file)

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
                character = character_byte.decode(encoding=utils.shift_jis, errors='strict')
                decoded_string = decoded_string + character
                i = i + 1
            else:
                character_bytes = line[i:i + 2]
                if b'\x88\x9f' <= character_bytes <= b'\xea\xa0':
                    decoded_character = self.decode(character_bytes)
                    decoded_string = decoded_string + decoded_character
                else:
                    character = character_bytes.decode(encoding=utils.shift_jis, errors='strict')
                    decoded_string = decoded_string + character
                i = i + 2
        return decoded_string

    def read_script_from_file(self, filename):
        with open(filename, mode='rb') as f:
            return self.read_script(f.read())


def subtract_bytes(bytes1: bytes, bytes2: bytes):
    int1 = int.from_bytes(bytes1, byteorder='big')
    int2 = int.from_bytes(bytes2, byteorder='big')
    result = int1 - int2
    return result


def write_text_file(filename, script: str):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(script)


def decode_files(decoder: Decoder, in_path, out_path):
    makedirs(out_path, exist_ok=True)
    for f in utils.get_scripts(in_path):
        print(f)
        in_filename = join(in_path, f)
        out_filename = join(out_path, f)
        decoded_script = decoder.read_script_from_file(in_filename)
        write_text_file(out_filename, decoded_script)


def decode(folder, character_encoding_file='wa2.chs.txt'):
    decoder = Decoder(character_encoding_file)
    out_folder = f'{folder}_decoded'
    decode_files(decoder, folder, out_folder)
    return out_folder
