import sys
from os import listdir, makedirs
from os.path import isfile, join
from decoder import Decoder
import re

shift_jis = "shift-jis"


def get_scripts(path):
    return [f for f in listdir(path) if isfile(join(path, f)) and re.match(r"^[\d_]+.txt$", f)]


def read_text_file(filename: str):
    with open(filename, mode='r', encoding='utf-8') as f:
        return f.read()


def write_text_file(filename: str, script: str):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(script)


def decode_files(decoder: Decoder, in_path, out_path):
    makedirs(out_path, exist_ok=True)
    for f in get_scripts(in_path):
        print(f)
        in_filename = join(in_path, f)
        out_filename = join(out_path, f)
        decoded_script = decoder.read_script_from_file(in_filename)
        write_text_file(out_filename, decoded_script)


def encode_files(decoder: Decoder, in_path, out_path):
    makedirs(out_path, exist_ok=True)
    for f in get_scripts(in_path):
        print(f)
        in_filename = join(in_path, f)
        out_filename = join(out_path, f)
        text_script = read_text_file(in_filename)
        decoder.write_script_to_file(out_filename, text_script)


def main(command, folder, character_encoding_file='res/wa2.chs.txt'):
    decoder = Decoder(character_encoding_file)
    if command == 'decode':
        out_folder = f'{folder}_decoded'
        decode_files(decoder, folder, out_folder)
        return out_folder
    elif command == 'encode':
        out_folder = f'{folder}_encoded'
        encode_files(decoder, folder, out_folder)
        return out_folder


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3:
        print("usage: python decode.py command input_folder character_encoding_file")
        print("  command: encode or decode")
        print("  input_folder: folder containing the decoded/encoded scripts")
        print("  character_encoding_file: Text file containing character encodings. e.g. res/wa2.chs.txt")
    else:
        main(args[0], args[1], args[2])

