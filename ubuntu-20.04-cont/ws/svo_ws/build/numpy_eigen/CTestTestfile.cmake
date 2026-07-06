# CMake generated Testfile for 
# Source directory: /workspace/svo_ws/src/numpy_eigen
# Build directory: /workspace/svo_ws/build/numpy_eigen
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_numpy_eigen_nosetests_test.numpy_eigen_tests.py "/workspace/svo_ws/build/numpy_eigen/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/workspace/svo_ws/build/numpy_eigen/test_results/numpy_eigen/nosetests-test.numpy_eigen_tests.py.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /workspace/svo_ws/build/numpy_eigen/test_results/numpy_eigen" "/usr/bin/nosetests3 -P --process-timeout=60 /workspace/svo_ws/src/numpy_eigen/test/numpy_eigen_tests.py --with-xunit --xunit-file=/workspace/svo_ws/build/numpy_eigen/test_results/numpy_eigen/nosetests-test.numpy_eigen_tests.py.xml")
set_tests_properties(_ctest_numpy_eigen_nosetests_test.numpy_eigen_tests.py PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/catkin/cmake/test/nosetests.cmake;83;catkin_run_tests_target;/workspace/svo_ws/src/numpy_eigen/CMakeLists.txt;25;catkin_add_nosetests;/workspace/svo_ws/src/numpy_eigen/CMakeLists.txt;0;")
subdirs("gtest")
