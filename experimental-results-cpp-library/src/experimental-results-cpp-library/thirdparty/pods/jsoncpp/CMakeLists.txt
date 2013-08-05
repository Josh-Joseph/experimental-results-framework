cmake_minimum_required(VERSION 2.6.0)

# pull in the pods macros. See cmake/pods.cmake for documentation
set(POD_NAME jsoncpp)
include(cmake/pods.cmake)

# This assumes that the special fetch-amd-make Makefile target has
#  already run, which provides the files used here.
include_directories( BEFORE jsoncpp-src-0.6.0-rc2/dist )
add_definitions(-DJSON_IS_AMALGAMATION)
add_library( jsoncpp SHARED
    jsoncpp-src-0.6.0-rc2/dist/jsoncpp.cpp
)

pods_install_headers(
    jsoncpp-src-0.6.0-rc2/dist/json/json.h
    jsoncpp-src-0.6.0-rc2/dist/json/json-forwards.h
    DESTINATION
    json
)
pods_install_libraries( jsoncpp )
pods_install_pkg_config_file(jsoncpp
    CFLAGS "-DJSON_IS_AMALGAMATION"
    LIBS -ljsoncpp
    REQUIRES
    VERSION 0.6.0)
