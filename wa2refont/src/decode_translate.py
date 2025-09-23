from os import listdir, makedirs
from os.path import isfile, join
from decoder import Decoder
import re
import argparse

from decoder_translator import DecoderTranslator
from encoder import Encoder


special_contents_numbers = [
    4000, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008, 4009,  # 不倶戴天の君へ
    5000, 5001, 5002, 5003, 5004,  # 雪が解け、そして雪が降るまで
    5100, 5101, 5102, 5103, 5104,  # 歌を忘れた偶像
    5200, 5201, 5202, 5203, 5204, 5205, 5206, 5207, 5208, 5209,  # Twinkle Snow～夢想～
    5301, 5302, 5303,  # 祭りの後～雪菜の三十分～
    5400, 5401,  # 彼の神様、あいつの救世主
    6001, 6002, 6003, 6004, 6005,  # 幸せへと戻る道
    6101, 6102, 6103, 6104,  # 幸せへと進む道
    7000,  # 雪菜姫の受難と大臣の悪巧み
    7100,  # 台風一過の小春日和
    7200,  # もう、ホワイトアルバムの季節じゃない
    7300   # 届かない恋、届いた
]


def filename_matches_special_contents(filename):
    for number in special_contents_numbers:
        if filename.startswith(str(number)):
            return True


def get_scripts(path, is_special_contents: bool):
    if is_special_contents:
        return [f for f in listdir(path) if isfile(join(path, f)) and re.match(r"^[\d_]+.txt$", f) and filename_matches_special_contents(f)]
    else:
        return [f for f in listdir(path) if isfile(join(path, f)) and re.match(r"^[\d_]+.txt$", f)]


def read_files(decoder: Decoder, path):
    files = {f: decoder.read_script_from_file(join(path, f)) for f in get_scripts(path)}
    sorted_files = dict(sorted(files.items(), key=lambda item: item[0]))
    return sorted_files


def recode_files(decoder: DecoderTranslator, encoder: Encoder, in_path, out_path, is_special_contents: bool):
    makedirs(out_path, exist_ok=True)

    for f in get_scripts(in_path, is_special_contents):
        print(f)
        file = join(in_path, f)
        translated_script = decoder.read_script_from_file(file)
        # print(translated_script)
        encoder.write_script_to_file(join(out_path, f), translated_script)


def main(in_path, out_path, is_special_contents: bool):
    decoder = DecoderTranslator(input_character_encoding_file='wa2.chs.txt',
                                output_character_encoding_file='wa2.cht.txt')
    encoder = Encoder(character_encoding_file='wa2.cht.txt')

    recode_files(decoder, encoder, in_path, out_path, is_special_contents)

    decoded_scripts = read_files(decoder, in_path)
    with open("decoded.txt", "w", encoding='utf-8') as f:
        f.writelines(filename + '\n' + s.replace('\\n', '\n') + '\n' for filename, s in decoded_scripts.items())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wa2refont')
    parser.add_argument('in_path', help='Input Directory')
    parser.add_argument('out_path', help='Output Directory')
    parser.add_argument('--special_contents', action='store_true', help='Recode Special Contents')
    args = parser.parse_args()
    main(args.in_path, args.out_path, args.special_contents)
