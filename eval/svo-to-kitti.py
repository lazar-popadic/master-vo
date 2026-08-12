#!/usr/bin/env python3
"""
Convert SVO odometry .txt to KITTI format
Usage: python svo-to-kitti.py odom.txt
       python svo-to-kitti.py ../data/odom.txt
       python svo-to-kitti.py /absolute/path/to/odom.txt
Output: <input_filename>_kitti.txt in same directory as input
"""

import numpy as np
import sys
import os
from scipy.spatial.transform import Rotation as R

def quaternion_to_rotation_matrix(qx, qy, qz, qw):
    quat = [qx, qy, qz, qw]
    rotation = R.from_quat(quat)
    return rotation.as_matrix()

def convert_vo_to_kitti(input_file):
    # Get directory and base name from input path
    input_dir = os.path.dirname(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(input_dir, f"{base_name}_kitti.txt")
    
    count = 0
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('#') or not line.strip():
                continue
            
            parts = line.strip().split()
            if len(parts) < 9:
                continue
            
            try:
                frame_id = int(parts[0])
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4])
                qx = float(parts[5])
                qy = float(parts[6])
                qz = float(parts[7])
                qw = float(parts[8])
                
                R_mat = quaternion_to_rotation_matrix(qx, qy, qz, qw)
                
                T = np.eye(4)
                T[0:3, 0:3] = R_mat
                T[0:3, 3] = [x, y, z]
                T_flat = T[0:3, :].flatten()
                
                pose_str = ' '.join([f'{val:.12f}' for val in T_flat])
                f_out.write(f"{frame_id} {pose_str}\n")
                count += 1
                
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing line: {line.strip()}")
                continue
    
    print(f"Converted {count} VO poses from {input_file} to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vo_to_kitti.py <input_file>")
        print("Example: python vo_to_kitti.py odom.txt")
        print("         python vo_to_kitti.py ../data/odom.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    convert_vo_to_kitti(input_file)