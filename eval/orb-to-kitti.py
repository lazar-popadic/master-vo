#!/usr/bin/env python3
"""
Convert ORB-SLAM3 trajectory (timestamp x y z qx qy qz qw) to KITTI format
ORB-SLAM3 outputs camera-to-world transform, so no inversion needed
Usage: python orb-to-kitti.py trajectory.txt
Output: trajectory_kitti.txt
"""

import numpy as np
import sys
import os
from scipy.spatial.transform import Rotation as R

def quaternion_to_rotation_matrix(qx, qy, qz, qw):
    quat = [qx, qy, qz, qw]
    rotation = R.from_quat(quat)
    return rotation.as_matrix()

def convert_orb_to_kitti(input_file):
    input_dir = os.path.dirname(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(input_dir, f"{base_name}_kitti.txt")
    
    count = 0
    
    # Coordinate transformation for ORB-SLAM3 to KITTI
    # ORB-SLAM3: X=right, Y=down, Z=forward
    # KITTI:     X=forward, Y=left, Z=up
    P = np.array([
        [0, 0, 1],   # new X = old Z
        [-1, 0, 0],  # new Y = -old X
        [0, -1, 0]   # new Z = -old Y
    ])
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('#') or not line.strip():
                continue
            
            parts = line.strip().split()
            if len(parts) < 8:
                continue
            
            try:
                # ORB-SLAM3 format: timestamp x y z qx qy qz qw
                timestamp = float(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                qx = float(parts[4])
                qy = float(parts[5])
                qz = float(parts[6])
                qw = float(parts[7])
                
                # Convert quaternion to rotation matrix
                R_mat = quaternion_to_rotation_matrix(qx, qy, qz, qw)
                
                # ORB-SLAM3 is already camera-to-world, no inversion needed
                # Just apply coordinate transformation
                R_new = P @ R_mat @ P.T
                t_new = P @ np.array([x, y, z])
                
                # Create 3x4 matrix for KITTI
                T_final = np.eye(4)
                T_final[0:3, 0:3] = R_new
                T_final[0:3, 3] = t_new
                
                T_flat = T_final[0:3, :].flatten()
                
                pose_str = ' '.join([f'{val:.12f}' for val in T_flat])
                f_out.write(f"{count} {pose_str}\n")
                count += 1
                
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing line: {line.strip()}")
                continue
    
    print(f"Converted {count} ORB-SLAM3 poses from {input_file} to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python orb-to-kitti.py <trajectory_file>")
        print("Example: python orb-to-kitti.py CameraTrajectory.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    convert_orb_to_kitti(input_file)