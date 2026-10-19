
message(STATUS "Building carla client library")

find_package(Boost REQUIRED)
find_package(recastnavigation REQUIRED)
find_package(rpclib REQUIRED)
find_package(PNG REQUIRED)

if (WIN32)
  find_package(ZLIB REQUIRED)
endif()

file(GLOB carla_client_sources
  ${CARLA_SOURCE_FOLDER}/carla/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/client/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/client/detail/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/geom/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/image/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/nav/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/opendrive/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/opendrive/parser/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/pointcloud/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/road/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/road/element/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/road/general/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/road/object/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/road/signal/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/rpc/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/sensor/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/sensor/data/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/sensor/s11n/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/streaming/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/streaming/detail/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/streaming/detail/tcp/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/streaming/low_level/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/multigpu/*.cpp
  ${CARLA_SOURCE_FOLDER}/carla/trafficmanager/*.cpp
)

file(GLOB carla_thirdparty_sources
  ${CARLA_SOURCE_FOLDER}/third-party/odrSpiral/*.cpp
  ${CARLA_SOURCE_FOLDER}/third-party/pugixml/*.cpp
)

add_library(client
  ${carla_client_sources}
  ${carla_thirdparty_sources}
)

add_library(carla::client ALIAS client)

target_link_libraries(client
  boost::boost
  recastnavigation::recastnavigation
  rpclib::rpc
  PNG::PNG
)

if (WIN32)
  target_link_libraries(client
    ZLIB::ZLIB
    shlwapi.lib
  )
endif()

message(STATUS ${CARLA_SOURCE_FOLDER})

target_include_directories(
  client PUBLIC
      "$<BUILD_INTERFACE:${CARLA_SOURCE_FOLDER};${CARLA_SOURCE_FOLDER}/third-party>"
              $<INSTALL_INTERFACE:include>)


include(GNUInstallDirs)
install(
  TARGETS client
  EXPORT carlaTargets
  INCLUDES
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

# headers
install(DIRECTORY ${CARLA_SOURCE_FOLDER}/carla
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY ${CARLA_SOURCE_FOLDER}/third-party/
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(
  EXPORT carlaTargets
  FILE carlaTargets.cmake
  NAMESPACE carla::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME})

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/carlaConfigVersion.cmake"
  VERSION ${carla_VERSION}
  COMPATIBILITY AnyNewerVersion)

configure_package_config_file(
  ${CMAKE_SOURCE_DIR}/cmake/carlaConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/carlaConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME})

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/carlaConfig.cmake"
              "${CMAKE_CURRENT_BINARY_DIR}/carlaConfigVersion.cmake"
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME})
