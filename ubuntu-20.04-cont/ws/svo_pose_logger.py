#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
import csv

class PoseLogger:
    def __init__(self, output_file='svo_traj_estimate.txt'):
        self.output_file = output_file
        self.frame_count = 0
        
        # Open file for writing
        self.f = open(output_file, 'w')
        self.f.write("# frame_id timestamp x y z qx qy qz qw\n")
        
        # Subscribe to SVO pose
        rospy.Subscriber('/svo/pose_imu', PoseWithCovarianceStamped, self.pose_callback)
        rospy.loginfo(f"Logging poses to {output_file}")
    
    def pose_callback(self, msg):
        """Callback for pose messages"""
        # Extract data
        timestamp = msg.header.stamp.to_sec()
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation
        
        # Write to file: frame_id timestamp x y z qx qy qz qw
        line = f"{self.frame_count} {timestamp} {pos.x} {pos.y} {pos.z} {ori.x} {ori.y} {ori.z} {ori.w}\n"
        self.f.write(line)
        self.f.flush()
        
        self.frame_count += 1
        
        if self.frame_count % 100 == 0:
            rospy.loginfo(f"Logged {self.frame_count} poses")

if __name__ == '__main__':
    rospy.init_node('pose_logger')
    logger = PoseLogger()
    rospy.spin()
