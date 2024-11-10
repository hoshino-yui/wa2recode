from os.path import join
import utils
from os import makedirs
from code_map import code_maps


class Encoder:
    def __init__(self, character_encoding_file):
        self.character_encoding = utils.read_character_encoding(filename=character_encoding_file)

    def write_script_to_file(self, filename, script: str):
        with open(filename, mode='wb') as f:
            f.write(self.write_script(script))

    def write_script(self, script: str):
        script_bytes = b''
        for character in script:
            if character in self.character_encoding:
                character_byte = self.encode(character)
                script_bytes = script_bytes + character_byte
            else:
                character_byte = character.encode(encoding=utils.shift_jis, errors='strict')
                script_bytes = script_bytes + character_byte
        return script_bytes

    def encode(self, character):
        index = self.character_encoding.index(character)
        for start, end, loc in reversed(code_maps):
            if loc <= index:
                return add_bytes(start, int_to_bytes(index - loc))


def add_bytes(bytes1: bytes, bytes2: bytes):
    int1 = int.from_bytes(bytes1, byteorder='big')
    int2 = int.from_bytes(bytes2, byteorder='big')
    result = int1 + int2
    return int_to_bytes(result)


def int_to_bytes(int1):
    return int1.to_bytes(2, byteorder='big')


def encode_files(encoder: Encoder, in_path, out_path):
    makedirs(out_path, exist_ok=True)
    for f in utils.get_scripts(in_path):
        print(f)
        in_filename = join(in_path, f)
        out_filename = join(out_path, f)
        text_script = read_text_file(in_filename)
        encoder.write_script_to_file(out_filename, text_script)


def read_text_file(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        return f.read()


def encode(folder, character_encoding_file='wa2.chs.txt'):
    encoder = Encoder(character_encoding_file)
    out_folder = f'{folder}_encoded'
    encode_files(encoder, folder, out_folder)
    return out_folder
