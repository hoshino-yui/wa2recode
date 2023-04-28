# wa2recode

Tools for modifying the scripts and character encoding of the game White Album 2 (and theoretically  White Album 2 Special Contents).

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
1. Extract font sheets in TGA format from the game using wa2repack.
2. Convert the TGA formatted font sheets to BMP format. paint.net is the recommended tool.
3. Place the BMP formatted font sheets (14pt本体.bmp, 14pt袋.bmp, 本体80.bmp, 袋影80.bmp) into the font_sheets directory. 
4. Use following command to create new font sheets.
   ```
   cd wa2refont
   python src/refont.py
   ```
5. Use wa2repack to pack the font sheets. 

## wa2recode

Python scripts for the decoding and re-encoding of White Album 2 scripts in custom encoding.
Decoded scripts are encoded in UTF-8. 

### Usage
1. Extract scripts from the game using wa2repack.
2. Use following command to decode and re-encode scripts.
   ```
   cd wa2refont
   python src/decode.py decode scripts res/wa2.chs.txt
   python src/decode.py encode scripts_translated res/wa2.cht.txt
   ```
3. Use wa2repack to pack the scripts. 

# Acknowledgements
This project is built upon asmodean's great work of exkizpak.cpp. 
This project would not have existed without him.

Special thanks to Leaf for making the game, and to the translators for their hard work. 

# Context
Imagine the game is being translated into a simplified version of a language. 

You hope to enjoy the game in the traditional version of the language. 

It would be great if there is a way to replace the simplified characters in the game into proper characters. 

This tool does exactly that.

There are a few important files. 

    fnt.pak - Contains font sheets (file name and content Shift JIS encoded) - 14pt本体.tga, 14pt袋.tga, 本体80.tga, 袋影80.tga
    script.pak - As file name. (Scripts are stored in Shift JIS encoded TXT files, .bnr files are binary files unrelated to the project. )
    grp.pak - Graphical resources including menu buttons, texts, and artworks. 

The translated version of the game comes with a modified exe that reads these resources from a different file. 

    fon.pak - Equivalent of fnt.pak
    ck-gal.pak - Equivalent of script.pak
    grp directory - Partial equivalent of grp.pak

Warning: Make backups before you make any modifications.
