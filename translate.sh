#!/bin/bash

set -ex

cp myVolume/fnt.pak .
cp myVolume/script.pak .
cp myVolume/script_special.pak .

/wa2translate/wa2repack/build/wa2repack unpack fnt.pak
/wa2translate/wa2repack/build/wa2repack unpack script.pak
/wa2translate/wa2repack/build/wa2repack unpack script_special.pak

## Decompress font
mkdir fnt_decompressed
cp fnt/index fnt_decompressed/

while read -r filename
do
  if [[ $filename == *.tga ]]
  then
    echo Decompressing fnt/"$filename"
    filename_without_extension=$(basename "$filename" .tga)
    convert fnt/"$filename" fnt_decompressed/"$filename_without_extension".bmp
  else
    cp fnt/"$filename" fnt_decompressed/"$filename"
  fi
done < fnt/index

## Update font
ls fnt_decompressed
cp -R fnt_decompressed/. fnt_refont
/wa2translate/python/venv/bin/python wa2refont/src/refont.py fnt_refont
cp -R fnt_refont/. myVolume/fnt_refont


## Translate Script
cp -R script/. script_translated
/wa2translate/python/venv/bin/python wa2refont/src/decode_translate.py script script_translated

## Translate Script for Special Contents
cp -R script_special/. script_special_translated
/wa2translate/python/venv/bin/python wa2refont/src/decode_translate.py --special_contents script_special script_special_translated


## Repack Script
/wa2translate/wa2repack/build/wa2repack pack script_translated
cp script_translated.repacked.pak myVolume

## Repack Script for Special Contents
/wa2translate/wa2repack/build/wa2repack pack script_special_translated
cp script_special_translated.repacked.pak myVolume

## Repack font
/wa2translate/wa2repack/build/wa2repack pack fnt_refont
cp fnt_refont.repacked.pak myVolume
