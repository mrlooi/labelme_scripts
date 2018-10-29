cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

project(read_labelme_json)

set(CXX_COMPILE_FLAGS "-std=c++11 -w")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CXX_COMPILE_FLAGS}")

find_package(OpenCV REQUIRED)

add_executable (read_labelme_json read_labelme_json.cpp)
target_link_libraries (read_labelme_json ${OpenCV_LIBS})
