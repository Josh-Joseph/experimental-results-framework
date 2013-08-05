cmake_minimum_required(VERSION 2.6.0)

# pull in the pods macros. See cmake/pods.cmake for documentation
set(POD_NAME jsoncpp)
include(cmake/pods.cmake)

# This assumes that the special fetch-amd-make Makefile target has
#  already run, which provides the files used here.
add_library( jsoncpp SHARED
    dist/jsoncpp.cpp
)

pods_install_headers(
    dist/json/json.h
    dist/json/json-forward.h
    DESTINATION
    json
)
pods_install_libraries( jsoncpp )
pods_install_pkg_config_file(jsoncpp
    CFLAGS
    LIBS -ljsoncpp
    REQUIRES
    VERSION 0.6.0)
