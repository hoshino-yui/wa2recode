#include "kcap_types.h"
#include <experimental/filesystem>
#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <fcntl.h>
#include <unistd.h>
#include "lzss.h"
#include "pack.h"
#include "utils.h"
#include "lzss.h"

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
    index_file.close();

    for (std::string file: filenames) {
        std::string file_path(path + "/" + filename);
        if (!std::experimental::filesystem::exists(file_path)) {
            std::cerr << "Missing file: " << file_path << std::endl;
            exit(2);
        }
    }
    return filenames;
}

void pack(const std::string& pack_path, bool compress) {
    std::vector<std::string> files = read_index(pack_path);

    std::string packed_filename = pack_path + ".repacked.pak";
    std::string content_filename = packed_filename + ".tmp";
    create_empty_file(packed_filename);
    create_empty_file(content_filename);
    std::ofstream packed_file(packed_filename, std::ios::app | std::ios::binary);
    std::ofstream content_file(content_filename, std::ios::app | std::ios::binary);

    KCAPHDR hdr{};
    strncpy(hdr.signature, std::string("KCAP").c_str(), 4);
    hdr.unknown1 = 0x0;
    hdr.unknown2 = 0x0;
    hdr.entry_count = files.size();
    packed_file.write((char *) &hdr, sizeof(KCAPHDR));

    uint32_t offset = sizeof(KCAPHDR) + sizeof(KCAPENTRY) * hdr.entry_count;

    for (int i = 0; i < hdr.entry_count; i++) {
        std::string filename = files[i];
        std::string file_path(pack_path + "/" + filename);

        uint32_t file_size = get_file_size(file_path);
        KCAPENTRY entry{};
        strcpy(entry.filename, filename.c_str());
        entry.unknown1 = 0x0;
        entry.unknown2 = 0x0;
        entry.offset = offset;

        unsigned char* file_content = new unsigned char[file_size];
        int fd = open_or_die(file_path, O_RDONLY | O_BINARY);
        read(fd, (char*) file_content, file_size);

        if (compress) {
            int compressed_max_file_size = file_size + 4096;  // Sometimes the compressed file is larger than original.
            unsigned char* compressed_content = new unsigned char[compressed_max_file_size];
            uint32_t compressed_length = lzss(file_content, file_size, compressed_content, compressed_max_file_size);

            entry.compressed_flag = 0x1;
            entry.length = compressed_length + sizeof(DATAHDR);
            DATAHDR datahdr {
                .length = entry.length,  // Don't ask.
                .original_length = file_size
            };

            std::cout << "Compressing entry for " << entry.filename
                << " offset=" << entry.offset
                << " entry.length=" << entry.length
                << " datahdr.length=" << datahdr.length
                << " datahdr.original_length=" << datahdr.original_length
                << std::endl;

            packed_file.write((char*) &entry, sizeof(KCAPENTRY));
            content_file.write((char*) &datahdr, sizeof(DATAHDR));
            content_file.write((char*) compressed_content, compressed_length);
            delete [] compressed_content;
        } else {
            entry.compressed_flag = 0x0;
            entry.length = file_size;
            std::cout << "Computing entry for " << entry.filename << " offset=" << entry.offset << " " << "length=" << entry.length << std::endl;
            packed_file.write((char*) &entry, sizeof(entry));
            content_file.write((char*) file_content, file_size);
        }

        delete [] file_content;
        close(fd);

        offset = offset + entry.length;
    }

    content_file.close();
    append_from_file(packed_file, content_filename);
    packed_file.close();
    std::experimental::filesystem::remove(content_filename);
}