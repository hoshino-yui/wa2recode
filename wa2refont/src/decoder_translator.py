import collections

import utils
from translation_character_map import character_map
from translation_map import translate_map
from decoder import Decoder


class DecoderTranslator(Decoder):
    def __init__(self, input_character_encoding_file, output_character_encoding_file):
        super().__init__(input_character_encoding_file)
        self.output_character_encoding = utils.read_character_encoding(filename=output_character_encoding_file)
        self.translation_character_map = character_map.items()
        self.translation_map = translate_map.items()
        self.validate_output_character_encoding_duplicated_characters()
        self.validate_output_character_encoding_missing_characters()

    def read_script(self, line: bytes):
        decoded = super(DecoderTranslator, self).read_script(line)
        translated = self.translate(decoded)
        return translated

    def translate(self, line: str):
        for character, translated in self.translation_character_map:
            line = line.replace(character, translated)
        for phrase, translated in self.translation_map:
            line = line.replace(phrase, translated)
        return line

    def validate_output_character_encoding_duplicated_characters(self):
        duplicated_characters = [ch for ch, count in collections.Counter(self.output_character_encoding).items() if count > 1]
        if len(duplicated_characters) > 0:
            print("Duplicated characters:", "".join(duplicated_characters))
            exit(1)

    def validate_output_character_encoding_missing_characters(self):
        missing_characters = set()

        for character in self.character_encoding:
            translated = character_map[character] if character in character_map.keys() else character
            if translated not in self.output_character_encoding and not is_shift_jis_punctuation(translated):
                missing_characters.add(translated)

        for phrase, translated in self.translation_map:
            for character in translated:
                if character not in self.output_character_encoding and not is_shift_jis_punctuation(character):
                    missing_characters.add(character)

        if len(missing_characters) > 0:
            print("Missing characters:", "".join(missing_characters))
            exit(1)


def is_shift_jis_punctuation(character):
    shift_jis_character = character.encode(utils.shift_jis, errors='ignore')
    return shift_jis_character and shift_jis_character < b'\x82\x5f'
