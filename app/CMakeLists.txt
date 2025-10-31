# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Find Zephyr package - works with both ZEPHYR_BASE and west workspace
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(blinky)

target_sources(app PRIVATE src/main.c)

target_include_directories(app 
    PRIVATE ${CMAKE_SOURCE_DIR}/cfg 
)

# Add a custom post-build step to rename the hex file
#add_custom_command(
#    TARGET app
#    POST_BUILD
#    COMMAND ${CMAKE_COMMAND} -E copy
#    $<TARGET_FILE:zephyr_final.elf>
#    ${CMAKE_CURRENT_BINARY_DIR}/viser-runner.elf
#    COMMENT "Renaming zephyr.elf to viser-runner.elf"
#)