from PIL import Image, ImageFont, ImageDraw
import itertools
import os

import decoder


def remove_extension(filename):
    return os.path.splitext(filename)[0]


def replace_characters_on_image(input_file, block_size=40, font_type='GenSenRounded-R.ttc', font_size=28,
                                stroke_width=0, start_pos=748, show=False):
    font = ImageFont.truetype(font_type, font_size)
    character_width = character_height = block_size

    image = Image.open(input_file)
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
    image.save(remove_extension(input_file) + ".refont.tga", compression=None)


if __name__ == '__main__':
    text = decoder.read_character_encoding('res/wa2.cht.txt')
    replace_characters_on_image("font_sheets/�{��80.bmp", 40, 'GenSenRounded-R.ttc', 28, 0)
    replace_characters_on_image("font_sheets/�܉e80.bmp", 40, 'GenSenRounded-R.ttc', 28, 2)
    replace_characters_on_image("font_sheets/14pt�{��.bmp", 24, 'GenSenRounded-R.ttc', 12, 0)
    replace_characters_on_image("font_sheets/14pt��.bmp", 24, 'GenSenRounded-R.ttc', 12, 1)
