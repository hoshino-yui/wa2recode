from unittest import TestCase
import encoder
import decoder
from os.path import join

import utils


class Test(TestCase):
    def is_same_file(self, filename1, filename2):
        with open(filename1, mode='rb') as f1, open(filename2, mode='rb') as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_main(self):
        script_folder = 'script'
        script_decoded_folder = decoder.decode(script_folder)
        script_reencoded_folder = encoder.encode(script_decoded_folder)

        for f in utils.get_scripts(script_reencoded_folder):
            print(f)
            self.is_same_file(join(script_folder, f), join(script_reencoded_folder, f))
