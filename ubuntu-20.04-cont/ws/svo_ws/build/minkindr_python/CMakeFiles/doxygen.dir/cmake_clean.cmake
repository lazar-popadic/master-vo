file(REMOVE_RECURSE
  "/workspace/svo_ws/devel/.private/minkindr_python/lib/python3/dist-packages/minkindr/libminkindr_python.so"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/doxygen.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
