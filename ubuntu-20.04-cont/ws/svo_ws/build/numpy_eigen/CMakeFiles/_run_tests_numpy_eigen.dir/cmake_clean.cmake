file(REMOVE_RECURSE
  "/workspace/svo_ws/devel/.private/numpy_eigen/lib/python3/dist-packages/numpy_eigen/libnumpy_eigen.so"
  "/workspace/svo_ws/devel/.private/numpy_eigen/lib/python3/dist-packages/numpy_eigen/libnumpy_eigen_test.so"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/_run_tests_numpy_eigen.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
