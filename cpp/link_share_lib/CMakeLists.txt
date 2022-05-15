project(share_lib)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

add_library(a STATIC 
    src/aaa.cpp)

target_include_directories(a 
    PUBLIC 
    src/)

add_library(b SHARED
    src/bbb.cpp
)

target_include_directories(b
    PUBLIC
    src/
)

target_link_libraries(b
    PUBLIC
    -Wl,-dn
    ${PROJECT_SOURCE_DIR}/lib/liba.a
    -Wl,-dy
)

add_library(c SHARED
    src/ccc.cpp
)

target_include_directories(c
    PUBLIC
    src/
)

# target_link_libraries(c
#     PUBLIC
#     ${PROJECT_SOURCE_DIR}/lib/libb.so
#     ${PROJECT_SOURCE_DIR}/lib/liba.so
# )

target_link_libraries(c
    PUBLIC
    -Wl,--whole-archive
    ${PROJECT_SOURCE_DIR}/lib/libb.so
    -Wl,--no-whole-archive
)

add_executable(${PROJECT_NAME} src/main.cpp)

target_include_directories(${PROJECT_NAME}
    PRIVATE
    src/
)

# target_link_libraries(${PROJECT_NAME}
#     ${PROJECT_SOURCE_DIR}/lib/libc.so
#     ${PROJECT_SOURCE_DIR}/lib/libb.so
#     ${PROJECT_SOURCE_DIR}/lib/liba.so
# )

target_link_libraries(${PROJECT_NAME}
    -Wl,--whole-archive
    ${PROJECT_SOURCE_DIR}/lib/libc.so
    -Wl,--no-whole-archive
)

