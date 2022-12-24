# wa2recode

Tools for modifying the character encoding of the game White Album 2 (and theoretically  White Album 2 Special Contents).

## wa2repack

C++ programme for the unpacking and repacking of the game's .pak resource files.

### Usages
    cmake wa2repack
    wa2repack unpack fnt.pak
    wa2repack pack ./fnt

## wa2refont

Python script for replacing character encodings in a font sheet. 
Does not accept TGA files as input but outputs the result as a TGA image. 

### Usage

    replace_characters_on_image(input_file="font_sheets/本体80.tga", block_size=40, 
                                font_type='GenSenRounded-R.ttc', font_size=28,
                                stroke_width=0)

# Acknowledgements
This project is built upon asmodean's great work of exkizpak.cpp. 
This project would not have existed without him.

Special thanks to Leaf for making the game, and to the translators for their hard work. 

# Use Case
Imagine the game is being translated into a simplified version of a language. 

You hope to enjoy the game in the traditional version of the language. 

It would be great if there is a way to replace the simplified characters in the game into proper characters. 

This tool does exactly that. 

## Context
There are a few important files. 

    fnt.pak - Contains font sheets (file name and content Shift JIS encoded) - 14pt本体.tga, 14pt袋.tga, 本体80.tga, 袋影80.tga
    script.pak - As file name.
    grp.pak - Graphical resources including menu buttons, texts, and artworks. 

The translated version of the game comes with a modified exe that reads these resources from a different file. 

    fon.pak - Equivalent of fnt.pak
    ck-gal.pak - Equivalent of script.pak
    grp directory - Partial equivalent of grp.pak

## Usage
1. Warning: Make backups before you make any modifications.

2. Unpack fnt.pak (or fon.pak) with

    ```
   wa2repack unpack fnt.pak
    ```

3. Convert the TGA formatted font sheets to BMP format because the python script does not accept TGA images. paint.net is the recommended tool. 

4. Place the BMP font sheets in the font_sheets folder. Replace the simplified characters in the font sheets with proper characters using 

    ```
   python wa2refont/src/main.py
    ```
   
5. Place the modified font sheets back into the unpacked `fnt` folder. Repack the modified folder as `fnt.pak` with

    ```
   wa2repack pack ./fnt
   ```

6. Replace `fnt.pak` (or `fon.pak`) in the game directory with the modified one. If you choose to use the original `wa2.exe`, replace `script.pak` with `ck-gal.pak` extracted from the translated version. Save files are incompatible unless `ck-gal` is replaced with `script` using a binary editor.
