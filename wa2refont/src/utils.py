import os
from os.path import isfile, join
import re

shift_jis = "shift-jis"


def get_resource_file_path(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    path = path + '/../res/' + filename
    return path


def get_scripts(path):
    return [f for f in os.listdir(path) if isfile(join(path, f)) and re.match(r"^[\d_]+.txt$", f)]


def read_character_encoding(filename='wa2.cht.txt'):
    with open(get_resource_file_path(filename), 'r', encoding='utf-8') as file:
        return re.sub(r"\s", "", file.read(), flags=re.UNICODE)
