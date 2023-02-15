#include "utils.h"
#include <experimental/filesystem>
#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <sys/stat.h>
#include "lzss.h"

int open_or_die(const std::string& input_filename, int type) {
    const char *fn = input_filename.c_str();
    int fd = open(fn, type);
    if(fd == -1) {
        std::cerr << "Could not open " << fn << " (No such file or directory)" << std::endl;
        exit(1);
    }
    return fd;
}

void make_dir(std::string& path) {
    if (!std::experimental::filesystem::is_directory(path.c_str())) {
        mkdir(path.c_str(), 0777);
    }
}

void write_file(std::string path, const std::string& filename, unsigned char* buf, int len) {
    make_dir(path);
    std::string out_name = path + "/" + filename;
    std::fstream out_file(out_name, std::ios::out | std::ios::binary);
    out_file.write((char*) buf, len);
    out_file.close();
}

int get_file_size(const std::string& path) {
    return std::experimental::filesystem::v1::file_size(std::experimental::filesystem::path(path));
}

std::string remove_extension(const std::string& path) {
    return path.substr(0, path.length() - 4);
}

void append_from_file(std::ofstream& packed_file, const std::string& input_file) {
    std::ifstream input_file_stream(input_file, std::ios::app | std::ios::binary);
    packed_file << input_file_stream.rdbuf();
    input_file_stream.close();
}

void create_empty_file(const std::string& path) {
    std::ofstream file(path, std::ios::binary);
    file.close();
}