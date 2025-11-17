cmake_minimum_required(VERSION 4.1)
Set(CMAKE_CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_EXPORT_COMPILE_COMMANDS True)
set(CMAKE_CXX_CLANG_TIDY
  clang-tidy;
  -format-style='.clang-tidy';)
set(CMAKE_CXX_FLAGS_DEBUG_INIT "-g")

project(graph_colouring_benchmark)

include_directories(include)

add_executable(graph_colouring_benchmark src/graph_colouring_benchmark.cpp)
