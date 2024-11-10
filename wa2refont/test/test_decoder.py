from unittest import TestCase

from decoder import Decoder
from encoder import Encoder


class Test(TestCase):
    def test_round_trip(self):
        decoder = Decoder(character_encoding_file='wa2.cht.txt')
        encoder = Encoder(character_encoding_file='wa2.cht.txt')
        characters = decoder.character_encoding + "―：、』，『〜一髒"
        encoded_bytes = encoder.write_script(characters)
        decoded_characters = decoder.read_script(encoded_bytes)
        re_encoded_bytes = encoder.write_script(decoded_characters)
        self.assertEqual(decoded_characters, characters)
        self.assertEqual(re_encoded_bytes, encoded_bytes)
