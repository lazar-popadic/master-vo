#!/usr/bin/env python3
"""
Convert GT .csv to KITTI format using ORB-SLAM3 trajectory timestamps
Usage: python orb-gt-to-kitti.py gt.csv orb_trajectory.txt
Output: <gt_filename>_kitti.txt in same directory as gt input
"""

import pandas as pd
import numpy as np
import sys
import os
from scipy.interpolate import interp1d
import math

def planar_to_transformation_matrix(x, y, yaw):
    T = np.eye(4)
    R_mat = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw),  math.cos(yaw), 0],
        [0,             0,              1]
    ])
    T[0:3, 0:3] = R_mat
    T[0:3, 3] = [x, y, 0]
    return T[0:3, :]

def parse_timestamp(ts_str):
    ts_str_clean = ts_str.split('.')[0]
    ts_int = int(ts_str_clean)
    if ts_int > 1e12:
        return ts_int / 1e9
    else:
        return float(ts_str)

def interpolate_gt_to_vo_timestamps(gt_csv, vo_traj_txt):
    gt_dir = os.path.dirname(gt_csv)
    base_name = os.path.splitext(os.path.basename(gt_csv))[0]
    output_file = os.path.join(gt_dir, f"{base_name}_kitti.txt")
    
    gt_df = pd.read_csv(gt_csv)
    gt_df = gt_df.sort_values('timestamp')
    
    vo_data = []
    
    with open(vo_traj_txt, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 1:
                try:
                    ts_str = parts[0]
                    timestamp = parse_timestamp(ts_str)
                    vo_data.append((len(vo_data), timestamp))
                except Exception as e:
                    print(f"Warning: Could not parse line: {line.strip()}")
                    continue
    
    if not vo_data:
        print(f"Error: Could not read timestamps from {vo_traj_txt}")
        print("First few lines of file:")
        with open(vo_traj_txt, 'r') as f:
            for i, line in enumerate(f):
                if i < 5:
                    print(f"  {line.strip()}")
        sys.exit(1)
    
    vo_df = pd.DataFrame(vo_data, columns=['frame_id', 'timestamp'])
    
    print(f"Loaded GT: {len(gt_df)} poses from {gt_csv}")
    print(f"Loaded VO: {len(vo_df)} poses from {vo_traj_txt}")
    print(f"VO timestamp range: {vo_df['timestamp'].min():.6f} - {vo_df['timestamp'].max():.6f}")
    
    gt_t = gt_df['timestamp'].values
    gt_x = gt_df['x'].values
    gt_y = gt_df['y'].values
    gt_phi = gt_df['phi'].values
    
    gt_phi_unwrapped = np.unwrap(gt_phi)
    
    interp_x = interp1d(gt_t, gt_x, kind='linear', 
                        bounds_error=False, fill_value='extrapolate')
    interp_y = interp1d(gt_t, gt_y, kind='linear', 
                        bounds_error=False, fill_value='extrapolate')
    interp_phi = interp1d(gt_t, gt_phi_unwrapped, kind='linear', 
                          bounds_error=False, fill_value='extrapolate')
    
    vo_t = vo_df['timestamp'].values
    vo_frame_ids = vo_df['frame_id'].values
    
    gt_interp_x = interp_x(vo_t)
    gt_interp_y = interp_y(vo_t)
    gt_interp_phi = interp_phi(vo_t)
    
    count = 0
    with open(output_file, 'w') as f_out:
        for i in range(len(vo_t)):
            T = planar_to_transformation_matrix(
                gt_interp_x[i], 
                gt_interp_y[i], 
                gt_interp_phi[i]
            )
            T_flat = T.flatten()
            pose_str = ' '.join([f'{val:.12f}' for val in T_flat])
            f_out.write(f"{int(vo_frame_ids[i])} {pose_str}\n")
            count += 1
    
    print(f"Created {count} interpolated GT poses in {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python orb-gt-to-kitti.py <gt_csv> <orb_trajectory_txt>")
        print("Example: python orb-gt-to-kitti.py gt.csv CameraTrajectory.txt")
        sys.exit(1)
    
    gt_csv = sys.argv[1]
    vo_traj_txt = sys.argv[2]
    
    if not os.path.exists(gt_csv):
        print(f"Error: GT file '{gt_csv}' not found!")
        sys.exit(1)
    
    if not os.path.exists(vo_traj_txt):
        print(f"Error: VO file '{vo_traj_txt}' not found!")
        sys.exit(1)
    
    interpolate_gt_to_vo_timestamps(gt_csv, vo_traj_txt)