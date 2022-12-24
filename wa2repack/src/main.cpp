// originally exkizpak.cpp, v1.02, 2022/12/21, coded by asmodean

// contact:
//   web:   http://asmodean.reverse.net
//   email: asmodean [at] hush.com
//   irc:   asmodean on efnet (irc.efnet.net)

// Extracts KCAP (*.PAK) archives used by ???|????????|.

#include <iostream>
#include "unpack.h"
#include "pack.h"

int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "originally exkizpak v1.02 coded by asmodean\n\n");
        fprintf(stderr, "usage: %s unpack <input.pak>\n", argv[0]);
        fprintf(stderr, "usage: %s pack <./pack_folder>\n", argv[0]);
        return -1;
    }

    std::string command(argv[1]);
    std::string path(argv[2]);

    if (command == "unpack") {
        unpack(path);
        return 0;
    }
    if (command == "pack") {
        pack(path);
        return 0;
    }
    std::cerr << "Unknown command: " << command << std::endl;
    return 1;
}
