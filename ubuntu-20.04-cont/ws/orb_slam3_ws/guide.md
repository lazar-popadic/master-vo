sudo apt install libepoxy-dev
catkin build orb_slam3_ros --cmake-args -DPangolin_DIR=/workspace/Pangolin/build

roslaunch orb_slam3_ros ros381.launch bag_file:=/workspace/bags/curve_sequence_slow.bag
