from unittest import TestCase

from decoder_translator import is_shift_jis_punctuation
from encoder import Encoder


class Test(TestCase):
    def test_validate_character_encoding(self):
        self.assertTrue(is_shift_jis_punctuation('：'))
        self.assertTrue(is_shift_jis_punctuation('、'))
        self.assertTrue(is_shift_jis_punctuation('』'))
        self.assertTrue(is_shift_jis_punctuation('，'))
        self.assertTrue(is_shift_jis_punctuation('『'))
        self.assertTrue(is_shift_jis_punctuation('〜'))
        self.assertTrue(is_shift_jis_punctuation('６'))

        self.assertFalse(is_shift_jis_punctuation('一'))
        self.assertFalse(is_shift_jis_punctuation('髒'))

    def test_byte(self):
        encoder = Encoder(character_encoding_file='wa2.cht.txt')
        bytes1 = encoder.encode('湯')
        bytes2 = encoder.encode('煙')
        bytes3 = encoder.encode('雨')
        self.assertEqual(bytes1, b'\x93\x92')
        self.assertEqual(bytes2, b'\x89\x8c')
        self.assertEqual(bytes3, b'\x89\x4a')

