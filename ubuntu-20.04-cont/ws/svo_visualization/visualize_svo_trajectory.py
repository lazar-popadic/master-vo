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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = '/workspace/svo_visualization/straight_sequence_fast.txt'
    
    traj = load_trajectory(filepath)
    
    # Extract positions
    x = traj[:, 0]
    y = traj[:, 1]
    z = traj[:, 2]
    
    # Simple 2D plot - top down view
    plt.figure(figsize=(12, 10))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.scatter(x[0], y[0], color='green', s=100, label='Start', zorder=5)
    plt.scatter(x[-1], y[-1], color='red', s=100, label='End', zorder=5)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.title('2D Trajectory (Top View)')
    plt.legend()
    plt.show()
    
    # Also plot x and y separately over time to see straight lines
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    ax1.plot(x, 'b-', linewidth=1)
    ax1.set_ylabel('X (m)')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('X Position Over Time')
    
    ax2.plot(y, 'r-', linewidth=1)
    ax2.set_ylabel('Y (m)')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Y Position Over Time')
    ax2.set_xlabel('Frame Index')
    
    plt.tight_layout()
    plt.show()