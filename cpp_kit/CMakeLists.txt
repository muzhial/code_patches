cmake_minimum_required(VERSION 3.14.0)
project(cpp_kit VERSION 0.0.1 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_executable(main main.cpp)
