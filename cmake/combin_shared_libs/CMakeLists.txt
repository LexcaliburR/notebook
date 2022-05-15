project(hello_combine)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_CXX_STANDARD 14)
#######################################
# libA
#######################################

add_library(a_shared STATIC 
    src/aaa.cpp)

target_include_directories(a_shared
    PUBLIC 
    src/)

set_target_properties(a_shared PROPERTIES OUTPUT_NAME "a")

#######################################
# libB
#######################################

add_library(b_shared STATIC
    src/bbb.cpp
)

target_include_directories(b_shared
    PUBLIC
    src/
)

target_link_libraries(b_shared
    PUBLIC
    a_shared
)

set_target_properties( b_shared PROPERTIES OUTPUT_NAME "b")

#######################################
# libC
#######################################

add_library(c_shared STATIC
    src/ccc.cpp
)

target_include_directories(c_shared
    PUBLIC
    src/
)

target_link_libraries(c_shared
    b_shared
    a_shared
    )
set_target_properties(c_shared PROPERTIES OUTPUT_NAME "c")

######################################
# libmerge
######################################

add_library(merge_shared INTERFACE)

# target_include_directories(merge_shared PUBLIC ${PROJECT_SOURCE_DIR}/src)

target_link_libraries( merge_shared
    INTERFACE
    # -Wl,--whole-archive
    a_shared
    b_shared
    c_shared
    # -Wl,--no-whole-archive
)

#####################################################
# execute
#####################################################

add_executable(${PROJECT_NAME}_shared src/main.cpp)

target_include_directories(${PROJECT_NAME}_shared
    PRIVATE
    src/
)

target_link_libraries(${PROJECT_NAME}_shared
    c_shared
    )
