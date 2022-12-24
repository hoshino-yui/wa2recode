#include "kcap_types.h"
#include <experimental/filesystem>
#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include "lzss.h"
#include "pack.h"
#include "utils.h"

std::vector<std::string> read_index(const std::string& path) {
    std::string index_filename = path + "/index";
    std::ifstream index_file(index_filename.c_str(), std::ios::binary);
    if (index_file.fail()) {
        std::cerr << "Index file " << index_filename << " not found. It should list all files to pack. " << std::endl;
        exit(3);
    }
    std::vector<std::string> filenames;
    std::string filename;
    while (index_file >> filename) {
        filenames.push_back(filename);
    }
    return filenames;
}

void pack(const std::string& pack_path) {
    std::vector<std::string> files = read_index(pack_path);

    std::string packed_filename = pack_path + ".new.pak";
    create_empty_file(packed_filename);
    std::ofstream packed_file(packed_filename, std::ios::app | std::ios::binary);

    KCAPHDR hdr{};
    strncpy(hdr.signature, std::string("KCAP").c_str(), 4);
    hdr.unknown1 = 0x0;
    hdr.unknown2 = 0x0;
    hdr.entry_count = files.size();
    packed_file.write((char *) &hdr, sizeof(KCAPHDR));

    uint32_t offset = sizeof(KCAPHDR) + sizeof(KCAPENTRY) * hdr.entry_count;

    // TODO: Learn lzss
    for (int i = 0; i < hdr.entry_count; i++) {
        std::string file_path(pack_path + "/" + files[i]);
        if (!std::experimental::filesystem::exists(file_path)) {
            std::cerr << "Unable to pack " << file_path << std::endl;
            exit(2);
        }

        int file_size = get_file_size(file_path);
        KCAPENTRY entry{};
        strcpy(entry.filename, files[i].c_str());
        entry.length = file_size;
        entry.offset = offset;
        entry.unknown1 = 0x0;
        entry.unknown2 = 0x0;
        entry.compressed_flag = 0x0;
        std::cout << "Computing entry for " << entry.filename << " offset=" << offset << " " << "file_size=" << file_size << std::endl;

        packed_file.write((char *) &entry, sizeof(entry));
        offset = offset + file_size;
    }

    for (int i = 0; i < hdr.entry_count; i++) {
        std::string file_path(pack_path + "/" + files[i]);
        std::cout << "Packing " << file_path << std::endl;
        pack_file(packed_file, file_path);
    }

    packed_file.close();
}