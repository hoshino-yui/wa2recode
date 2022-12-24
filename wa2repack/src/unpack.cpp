#include "kcap_types.h"
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <string>
#include "utils.h"
#include "lzss.h"
#include <cstring>
#include <fstream>
#include "unpack.h"

int read_entry(int fd, KCAPENTRY entry, unsigned char** buf) {
    if (entry.compressed_flag) {
        lseek(fd, entry.offset, SEEK_SET);

        DATAHDR datahdr{};
        read(fd, &datahdr, sizeof(datahdr));

        int original_length = datahdr.original_length;
        int compressed_length = entry.length - sizeof(datahdr);

        unsigned char* compressed_buff = new unsigned char[compressed_length];
        read(fd, compressed_buff, compressed_length);

        unsigned char* decompressed_buff = new unsigned char[original_length];
        unlzss(compressed_buff, compressed_length, decompressed_buff, original_length);

        delete [] compressed_buff;

        *buf = decompressed_buff;

        return datahdr.original_length;
    } else {
        lseek(fd, entry.offset, SEEK_SET);

        unsigned char* buff = new unsigned char[entry.length];
        read(fd, buff, entry.length);

        *buf = buff;

        return entry.length;
    }
}

void write_unpacked_index(const std::string& out_folder, KCAPENTRY* entries, int len) {
    std::ofstream out_index_file(out_folder + "/index", std::ios::out | std::ios::binary);
    for (uint32_t i = 0; i < len; i++) {
        if (entries[i].length) {
            out_index_file << entries[i].filename << std::endl;
        }
    }
    out_index_file.close();
}

void unpack(const std::string& in_filename) {
    std::string out_folder = remove_extension(in_filename);
    int fd = open_or_die(in_filename, O_RDONLY | O_BINARY);

    KCAPHDR hdr;
    read(fd, &hdr, sizeof(hdr));

    if (memcmp(hdr.signature, "KCAP", 4)) {
        fprintf(stderr, "%s: not a KCAP archive (might be WMV video)\n", in_filename.c_str());
        exit(0);
    }

    std::cout << "File entry count = " << hdr.entry_count << std::endl;

    KCAPENTRY* entries = new KCAPENTRY[hdr.entry_count];
    read(fd, entries, sizeof(KCAPENTRY) * hdr.entry_count);

    for (uint32_t i = 0; i < hdr.entry_count; i++) {
        if (!entries[i].length) {
            std::cout << "Skipping " << entries[i].filename << " because it is probably a folder. " << std::endl;
            continue;
        }

        unsigned char* buff;

        int len = read_entry(fd, entries[i], &buff);

        std::cout << "Unpacking " << entries[i].filename << std::endl;

        write_file(out_folder, entries[i].filename, buff, len);

        delete [] buff;
    }
    write_unpacked_index(out_folder, entries, hdr.entry_count);

    delete [] entries;

    close(fd);
}