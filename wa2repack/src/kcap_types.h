#ifndef WA2REPACK_KCAP_TYPES_H
#define WA2REPACK_KCAP_TYPES_H

#include <cstdint>

struct KCAPHDR {
    char signature[4]; // "KCAP"
    uint32_t unknown1;
    uint32_t unknown2;
    uint32_t entry_count;
};

struct KCAPENTRY {
    uint32_t compressed_flag;
    char     filename[24];
    uint32_t unknown1;
    uint32_t unknown2;
    uint32_t offset;
    uint32_t length;
};

struct DATAHDR {
    uint32_t length;
    uint32_t original_length;
};
#endif //WA2REPACK_KCAP_TYPES_H
