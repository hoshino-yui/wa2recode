import itertools
import os
import sys
import shutil

from PIL import Image, ImageFont, ImageDraw

import utils

text = utils.read_character_encoding('wa2.cht.txt')


def remove_extension(filename):
    return os.path.splitext(filename)[0]


def replace_characters_on_image(input_file, output_file, block_size=40, font_size=28, stroke_width=0,
                                font_type='GenSenRounded-R.ttc', start_pos=748, show=False):
    font = ImageFont.truetype(utils.get_resource_file_path(font_type), font_size)
    character_width = character_height = block_size

    image = Image.open(input_file.encode(utils.shift_jis))
    print(image.format, image.size, image.mode)
    width, height = image.size
    character_positions = list(itertools.product(range(0, height, character_height), range(0, width, character_width)))
    for i, (h, w) in enumerate(character_positions[start_pos:start_pos + len(text)]):
        d = ImageDraw.Draw(image)
        d.rectangle(((w, h), (w+character_width, h+character_height)), fill=(0, 0, 0, 0))
        d.text((w + (character_width - font_size) / 2 - 1, h + (character_height - font_size) / 2 - 2),
               text[i], font=font, fill=(255, 255, 255, 255), stroke_width=stroke_width)
    if show:
        image.show()
    image.save('/tmp/tmp.tga', compression=None)
    shutil.move('/tmp/tmp.tga', output_file.encode(utils.shift_jis))


def main(folder):
    replace_characters_on_image(folder + "/14pt本体.bmp", folder + "/14pt本体.tga", 24, 12, 0)
    replace_characters_on_image(folder + "/14pt袋.bmp", folder + "/14pt袋.tga", 24, 12, 1)
    replace_characters_on_image(folder + "/本体80.bmp", folder + "/本体80.tga", 40, 28, 0)
    replace_characters_on_image(folder + "/袋影80.bmp", folder + "/袋影80.tga", 40, 28, 2)


if __name__ == '__main__':
    main(sys.argv[1])
