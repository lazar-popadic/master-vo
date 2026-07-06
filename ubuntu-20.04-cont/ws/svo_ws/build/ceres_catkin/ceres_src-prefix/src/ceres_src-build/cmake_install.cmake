# Install script for directory: /workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/workspace/svo_ws/devel/.private/ceres_catkin")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ceres" TYPE FILE FILES
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/autodiff_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/autodiff_local_parameterization.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/c_api.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/ceres.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/conditioned_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/context.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/cost_function_to_functor.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/covariance.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/crs_matrix.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/cubic_interpolation.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/dynamic_autodiff_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/dynamic_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/dynamic_cost_function_to_functor.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/dynamic_numeric_diff_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/evaluation_callback.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/fpclassify.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/gradient_checker.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/gradient_problem.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/gradient_problem_solver.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/iteration_callback.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/jet.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/local_parameterization.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/loss_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/normal_prior.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/numeric_diff_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/numeric_diff_options.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/ordered_groups.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/problem.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/rotation.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/sized_cost_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/solver.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/tiny_solver.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/tiny_solver_autodiff_function.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/tiny_solver_cost_function_adapter.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/types.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/version.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ceres/internal" TYPE FILE FILES
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/autodiff.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/disable_warnings.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/eigen.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/fixed_array.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/macros.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/manual_constructor.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/numeric_diff.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/port.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/reenable_warnings.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/scoped_ptr.h"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/include/ceres/internal/variadic_evaluate.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ceres/internal" TYPE FILE FILES "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/config/ceres/internal/config.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres/CeresTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres/CeresTargets.cmake"
         "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/CMakeFiles/Export/lib/cmake/Ceres/CeresTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres/CeresTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres/CeresTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres" TYPE FILE FILES "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/CMakeFiles/Export/lib/cmake/Ceres/CeresTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres" TYPE FILE FILES "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/CMakeFiles/Export/lib/cmake/Ceres/CeresTargets-release.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres" TYPE FILE RENAME "CeresConfig.cmake" FILES "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/CeresConfig-install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Ceres" TYPE FILE FILES
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/CeresConfigVersion.cmake"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/cmake/FindEigen.cmake"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/cmake/FindGlog.cmake"
    "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src/cmake/FindGflags.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/internal/ceres/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/workspace/svo_ws/build/ceres_catkin/ceres_src-prefix/src/ceres_src-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
