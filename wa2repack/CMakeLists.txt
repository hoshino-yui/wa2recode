cmake_minimum_required(VERSION 3.10)
project(wa2repack)

set(CMAKE_CXX_STANDARD 17)
link_libraries(stdc++fs)

# I have no idea how this works
add_executable(wa2repack src/main.cpp src/lzss.cpp src/utils.cpp src/pack.cpp src/unpack.cpp)
