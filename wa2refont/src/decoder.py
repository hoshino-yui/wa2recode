import utils
import code_map
from os import makedirs
from os.path import join


class Decoder:
    def __init__(self, character_encoding_file):
        self.character_encoding = utils.read_character_encoding(filename=character_encoding_file)
        self.character_bytes_start, self.character_bytes_end = self.calculate_character_byte_range()

    def calculate_character_byte_range(self):
        start = code_map.get_bytes_from_index(0)
        end = code_map.get_bytes_from_index(len(self.character_encoding) - 1)
        return start, end

    def decode(self, character_bytes):
        if character_bytes < self.character_bytes_start or character_bytes > self.character_bytes_end:
            decoded_character = character_bytes.decode(encoding=utils.shift_jis, errors='strict')
            if b'\x88\x9f' <= character_bytes <= b'\x9c\xff':
                print("WTF. Found SJIS kanji. " + decoded_character)
            return decoded_character

        return self.character_encoding[code_map.get_index_from_bytes(character_bytes)]

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
                decoded_character = self.decode(character_bytes)
                decoded_string = decoded_string + decoded_character
                i = i + 2
        return decoded_string

    def read_script_from_file(self, filename):
        with open(filename, mode='rb') as f:
            return self.read_script(f.read())


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
