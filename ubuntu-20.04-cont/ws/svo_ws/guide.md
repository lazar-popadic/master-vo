# KITTI in svo pro open
python3 /workspace/svo_ws/src/rpg_svo_pro_open/svo_ros/scripts/kitti_to_rosbag.py bag \
  --image-dir /path/to/KITTI/sequences/00/image_00 \
  --timestamps /path/to/KITTI/sequences/00/times.txt \
  --output /path/to/kitti_00_left.bag \
  --topic /camera/image_raw \
  --frame-id camera \
  --write-camera-info \
  --camera-info-topic /camera/camera_info \
  --calib-file /path/to/KITTI/calib.txt
  
  python3 /workspace/svo_ws/src/rpg_svo_pro_open/svo_ros/scripts/kitti_to_rosbag.py calib \
  --kitti-calib /path/to/KITTI/calib.txt \
  --output /workspace/svo_ws/src/rpg_svo_pro_open/svo_ros/param/calib/kitti_left.yaml \
  --camera-index 0 \
  --image-width 1241 \
  --image-height 376 \
  --distortion-type none