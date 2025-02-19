# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_swarm_com_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED swarm_com_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(swarm_com_FOUND FALSE)
  elseif(NOT swarm_com_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(swarm_com_FOUND FALSE)
  endif()
  return()
endif()
set(_swarm_com_CONFIG_INCLUDED TRUE)

# output package information
if(NOT swarm_com_FIND_QUIETLY)
  message(STATUS "Found swarm_com: 0.0.0 (${swarm_com_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'swarm_com' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${swarm_com_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(swarm_com_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${swarm_com_DIR}/${_extra}")
endforeach()
