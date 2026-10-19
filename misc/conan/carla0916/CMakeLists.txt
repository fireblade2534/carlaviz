cmake_minimum_required(VERSION 3.14)

if(NOT CARLA_VERSION)
  set(CARLA_VERSION "0.9.14")
endif()

project(
  carla
  VERSION ${CARLA_VERSION}
  DESCRIPTION "libcarla"
  LANGUAGES CXX)

option(CARLA_BUILD_CLIENT "Build carla client library" ON)
option(CARLA_BUILD_SERVER "Build carla client library" OFF)

set(CMAKE_CXX_STANDARD 20)

set(CARLA_SOURCE_FOLDER ${CMAKE_CURRENT_SOURCE_DIR}/LibCarla/source)

add_subdirectory("cmake/src")

if(CARLA_BUILD_TESTS)
  enable_testing()
  add_subdirectory("cmake/tests")
endif()
