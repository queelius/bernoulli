cmake_minimum_required(VERSION 3.14)
project(bernoulli_data_type
    VERSION 0.1.0
    DESCRIPTION "A probabilistic framework for approximate data types"
    LANGUAGES CXX)

# Header-only INTERFACE library
add_library(bernoulli INTERFACE)
add_library(bernoulli::bernoulli ALIAS bernoulli)

target_include_directories(bernoulli INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

target_compile_features(bernoulli INTERFACE cxx_std_17)

# Doxygen documentation target
find_package(Doxygen QUIET)
if(DOXYGEN_FOUND)
    configure_file(Doxyfile.in Doxyfile @ONLY)
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Generating API documentation with Doxygen")
endif()

# Tests (disabled by default — code does not compile yet)
option(BUILD_TESTING "Build tests" OFF)
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()
