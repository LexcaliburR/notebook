project(share_lib)
cmake_minimum_required(VERSION 3.5)


set(CMAKE_BUILD_TYPE Release)

add_library(a SHARED
    src/aaa.cpp
)

target_include_directories(a
    PUBLIC
    src/
)

add_library(b SHARED
    src/bbb.cpp
)

target_include_directories(b
    PUBLIC
    src/
)

target_link_libraries(b
    PUBLIC
    ${PROJECT_SOURCE_DIR}/build/liba.so
)

add_library(c SHARED
    src/ccc.cpp
)

target_include_directories(c
    PUBLIC
    src/
)

target_link_libraries(c
    ${PROJECT_SOURCE_DIR}/build/libb.so
    ${PROJECT_SOURCE_DIR}/build/liba.so
)

add_executable(${PROJECT_NAME} src/main.cpp)

target_include_directories(${PROJECT_NAME}
    PRIVATE
    src/
)

target_link_libraries(${PROJECT_NAME}
    ${PROJECT_SOURCE_DIR}/build/libc.so
    ${PROJECT_SOURCE_DIR}/build/libb.so
    ${PROJECT_SOURCE_DIR}/build/liba.so
)
