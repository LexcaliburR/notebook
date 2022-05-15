project(hello_combine)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_CXX_STANDARD 14)
#######################################
# libA
#######################################
add_library(a_static STATIC 
    src/aaa.cpp)

target_include_directories(a_static
    PUBLIC 
    src/)

set_target_properties(a_static PROPERTIES OUTPUT_NAME "a")

# add_library(a_shared SHARED 
#     src/aaa.cpp)

# target_include_directories(a_shared
#     PUBLIC 
#     src/)

# set_target_properties(a_shared PROPERTIES OUTPUT_NAME "a")

#######################################
# libB
#######################################
add_library(b_static 
    STATIC 
    src/bbb.cpp)

target_include_directories(b_static
    PUBLIC
    src/
)

target_link_libraries(b_static
    PUBLIC
    ${PROJECT_SOURCE_DIR}/build/liba.a
)
set_target_properties(b_static PROPERTIES OUTPUT_NAME "b")

# add_library(b_shared SHARED
#     src/bbb.cpp
# )

# target_include_directories(b_shared
#     PUBLIC
#     src/
# )

# target_link_libraries(b_shared
#     PUBLIC
#     -Wl,--whole-archive
#     ${PROJECT_SOURCE_DIR}/build/liba.so
#     -Wl,--no-whole-archive
#     )

# set_target_properties(b_static b_shared PROPERTIES OUTPUT_NAME "b" OUTPUT_NAME "b")

#######################################
# libC
#######################################
add_library(c_static STATIC
    src/ccc.cpp
)

target_include_directories(c_static
    PUBLIC
    src/
)

target_link_libraries(c_static
    PUBLIC
    ${PROJECT_SOURCE_DIR}/build/libb.a
    )
set_target_properties(c_static PROPERTIES OUTPUT_NAME "c")

# add_library(c SHARED
#     src/ccc.cpp
# )

# target_include_directories(c
#     PUBLIC
#     src/
# )

# target_link_libraries(c
#     PUBLIC
#     ${PROJECT_SOURCE_DIR}/build/libb.so
#     ${PROJECT_SOURCE_DIR}/build/liba.so
#     )
# set_target_properties(c_shared PROPERTIES OUTPUT_NAME "c")

######################################
# libmerge
######################################
add_library(merge_static STATIC ${PROJECT_SOURCE_DIR}/src/combin.cpp)
target_include_directories(merge_static PUBLIC ${PROJECT_SOURCE_DIR}/src)
target_link_libraries(merge_static
    PUBLIC
    -Wl,--whole-archive
    ${PROJECT_SOURCE_DIR}/lib/liba.a
    ${PROJECT_SOURCE_DIR}/lib/libb.a
    ${PROJECT_SOURCE_DIR}/lib/libc.a
    -Wl,--no-whole-archive
)

# add_library(merge_shared SHARED src/combin.cpp)

# target_include_directories(merge_shared PUBLIC ${PROJECT_SOURCE_DIR}/src)

# target_link_libraries( merge_shared
#     -Wl,--Bstatic,--whole-archive
#     # -Wl,--whole-archive
#     ${PROJECT_SOURCE_DIR}/lib/liba.a
#     ${PROJECT_SOURCE_DIR}/lib/libb.a
#     ${PROJECT_SOURCE_DIR}/lib/libc.a
#     -Wl,--no-whole-archive,-Bdynamic
#     # -Wl,-Bdynamic
# )

#####################################################
# execute
#####################################################
add_executable(${PROJECT_NAME}_static src/main.cpp)

target_include_directories(${PROJECT_NAME}_static
    PRIVATE
    src/
)

target_link_libraries(${PROJECT_NAME}_static
    merge_static
)

# add_executable(${PROJECT_NAME}_shared src/main.cpp)

# target_include_directories(${PROJECT_NAME}_shared
#     PRIVATE
#     src/
# )

# target_link_libraries(${PROJECT_NAME}_shared
#     merge_shared
# )
