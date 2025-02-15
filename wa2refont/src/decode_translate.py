import sys
from os import listdir, makedirs
from os.path import isfile, join
from decoder import Decoder
import re

from decoder_translator import DecoderTranslator
from encoder import Encoder


def get_scripts(path):
    return [f for f in listdir(path) if isfile(join(path, f)) and re.match(r"^[\d_]+.txt$", f)]


def read_files(decoder: Decoder, path):
    return {f: decoder.read_script_from_file(join(path, f)) for f in get_scripts(path)}


def recode_files(decoder: DecoderTranslator, encoder: Encoder, in_path, out_path):
    makedirs(out_path, exist_ok=True)
    for f in get_scripts(in_path):
        print(f)
        file = join(in_path, f)
        translated_script = decoder.read_script_from_file(file)
        # print(translated_script)
        encoder.write_script_to_file(join(out_path, f), translated_script)


def main(in_path, out_path):
    decoder = DecoderTranslator(input_character_encoding_file='wa2.chs.txt',
                                output_character_encoding_file='wa2.cht.txt')
    encoder = Encoder(character_encoding_file='wa2.cht.txt')

    recode_files(decoder, encoder, in_path, out_path)

    decoded_scripts = read_files(decoder, in_path)
    with open("decoded.txt", "w", encoding='utf-8') as f:
        f.writelines(filename + '\n' + s.replace('\\n', '\n') + '\n' for filename, s in decoded_scripts.items())


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
