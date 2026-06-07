# KITTI in svo pro open
python3 /workspace/svo_ws/src/rpg_svo_pro_open/svo_ros/scripts/kitti_to_rosbag.py calib \
  --kitti-calib /workspace/kitti/dataset/sequences/11/calib.txt \
  --output /workspace/svo_ws/src/rpg_svo_pro_open/svo_ros/param/calib/kitti_11.yaml \
  --camera-index 0 \
  --image-width 1226 \
  --image-height 370 \
  --distortion-type none

python3 /workspace/svo_ws/src/rpg_svo_pro_open/svo_ros/scripts/kitti_to_rosbag.py bag \
  --image-dir /workspace/kitti/dataset/sequences/11/image_0/ \
  --timestamps /workspace/kitti/dataset/sequences/11/times.txt \
  --output /workspace/kitti/dataset/kitti_11_left.bag \
  --topic /camera/image_raw \
  --frame-id camera \
  --write-camera-info \
  --camera-info-topic /camera/camera_info \
  --calib-file /workspace/kitti/dataset/sequences/11/calib.txt

roslaunch svo_ros run_from_bag.launch cam_name:=kitti_00
rosbag play /workspace/kitti/dataset/kitti_00_left.bag --clock
