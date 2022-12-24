#ifndef WA2REPACK_UTILS_H
#define WA2REPACK_UTILS_H

#define O_BINARY 0x8000

#include <string>

int open_or_die(const std::string& input_filename, int type);
void make_dir(std::string& path);
void write_file(std::string path, const std::string& filename, unsigned char* buf, int len);
int get_file_size(const std::string& path);
std::string remove_extension(const std::string& path);
void pack_file(std::ofstream& packed_file, const std::string& input_file);
void create_empty_file(const std::string& path);

#endif //WA2REPACK_UTILS_H
