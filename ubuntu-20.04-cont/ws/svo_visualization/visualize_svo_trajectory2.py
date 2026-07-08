#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys

def load_trajectory(filepath):
    """Load SVO trajectory file"""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) >= 8:
                try:
                    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                    qx, qy, qz, qw = float(parts[5]), float(parts[6]), float(parts[7]), float(parts[8])
                    data.append([x, y, z, qx, qy, qz, qw])
                except:
                    continue
    return np.array(data)

def quaternion_to_yaw(qx, qy, qz, qw):
    """Convert quaternion to yaw angle (radians)"""
    return np.arctan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy * qy + qz * qz))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = '/workspace/svo_visualization/curve_sequence_medium.txt'
    
    traj = load_trajectory(filepath)
    
    # Extract data
    x = traj[:, 0]
    y = traj[:, 1]
    qx = traj[:, 3]
    qy = traj[:, 4]
    qz = traj[:, 5]
    qw = traj[:, 6]
    
    # Compute yaw in degrees
    yaw = np.rad2deg(quaternion_to_yaw(qx, qy, qz, qw))
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Plot 1: X and Y over time
    axes[0].plot(x, 'b-', linewidth=1.5, label='X')
    axes[0].plot(y, 'r-', linewidth=1.5, label='Y')
    axes[0].set_ylabel('Position (m)')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].set_title('X and Y Position Over Time')
    
    # Plot 2: Yaw over time
    axes[1].plot(yaw, 'g-', linewidth=1.5)
    axes[1].set_ylabel('Yaw (degrees)')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_title('Orientation (Yaw) Over Time')
    
    # Plot 3: 2D Trajectory
    axes[2].plot(x, y, 'b-', linewidth=1.5)
    axes[2].scatter(x[0], y[0], color='green', s=100, label='Start', zorder=5)
    axes[2].scatter(x[-1], y[-1], color='red', s=100, label='End', zorder=5)
    axes[2].grid(True, alpha=0.3)
    axes[2].axis('equal')
    axes[2].set_xlabel('X (m)')
    axes[2].set_ylabel('Y (m)')
    axes[2].set_title('2D Trajectory')
    axes[2].legend()
    
    plt.tight_layout()
    plt.show()