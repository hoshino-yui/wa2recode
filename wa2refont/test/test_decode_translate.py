from unittest import TestCase

import decode_translate


class Test(TestCase):
    def test_special_contents(self):
        self.assertTrue(decode_translate.filename_matches_special_contents('4001'))
        self.assertFalse(decode_translate.filename_matches_special_contents('4101'))



