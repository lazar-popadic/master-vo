#!/usr/bin/env python3
"""
Plot KITTI format trajectory in 2D top-down view
Usage: python plot_trajectory.py <kitti_file.txt>
Example: python plot_trajectory.py odom_kitti.txt
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def read_kitti_trajectory(file_path):
    """
    Read KITTI format trajectory file
    Format: frame_id T00 T01 T02 T03 T10 T11 T12 T13 T20 T21 T22 T23
    Returns: array of (x, y) positions
    """
    positions = []
    frame_ids = []
    
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            
            parts = line.strip().split()
            
            # Check if format has frame_id or just pose
            if len(parts) == 13:
                # Format: frame_id + 12 pose values
                frame_id = int(parts[0])
                T = np.array([float(x) for x in parts[1:13]]).reshape(3, 4)
                frame_ids.append(frame_id)
            elif len(parts) == 12:
                # Format: just 12 pose values (no frame_id)
                T = np.array([float(x) for x in parts]).reshape(3, 4)
                frame_ids.append(len(positions))
            else:
                print(f"Warning: Skipping line with {len(parts)} values")
                continue
            
            # Extract translation (x, y) from the 3x4 matrix
            x = T[0, 3]
            y = T[1, 3]
            positions.append((x, y))
    
    return np.array(positions), np.array(frame_ids)

def plot_trajectory(positions, frame_ids, title="Trajectory (Top-Down View)"):
    """
    Plot 2D trajectory
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot trajectory
    ax.plot(positions[:, 0], positions[:, 1], 'b-', linewidth=2, label='Trajectory')
    
    # Mark start position
    ax.plot(positions[0, 0], positions[0, 1], 'go', markersize=10, label='Start')
    
    # Mark end position
    ax.plot(positions[-1, 0], positions[-1, 1], 'ro', markersize=10, label='End')
    
    # Add arrows to show direction every N frames
    step = max(1, len(positions) // 50)
    for i in range(0, len(positions), step):
        if i + 1 < len(positions):
            dx = positions[i+1, 0] - positions[i, 0]
            dy = positions[i+1, 1] - positions[i, 1]
            # Only add arrow if movement is significant
            if np.sqrt(dx**2 + dy**2) > 0.01:
                ax.arrow(positions[i, 0], positions[i, 1], 
                        dx * 0.3, dy * 0.3,
                        head_width=0.03, head_length=0.05, 
                        fc='blue', ec='blue', alpha=0.3)
    
    # Labels and formatting
    ax.set_xlabel('X (meters)', fontsize=12)
    ax.set_ylabel('Y (meters)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    ax.legend()
    
    # Show frame numbers at start and end
    ax.text(positions[0, 0], positions[0, 1], f'  frame {frame_ids[0]}', 
            fontsize=10, color='green')
    ax.text(positions[-1, 0], positions[-1, 1], f'  frame {frame_ids[-1]}', 
            fontsize=10, color='red')
    
    plt.tight_layout()
    plt.show()

def plot_multiple_trajectories(file_paths, labels=None):
    """
    Plot multiple trajectories on the same plot for comparison
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    
    for i, file_path in enumerate(file_paths):
        positions, frame_ids = read_kitti_trajectory(file_path)
        
        color = colors[i % len(colors)]
        label = labels[i] if labels and i < len(labels) else os.path.basename(file_path)
        
        ax.plot(positions[:, 0], positions[:, 1], '-', color=color, 
                linewidth=2, label=label)
        
        # Mark start
        ax.plot(positions[0, 0], positions[0, 1], 'o', color=color, markersize=8)
    
    ax.set_xlabel('X (meters)', fontsize=12)
    ax.set_ylabel('Y (meters)', fontsize=12)
    ax.set_title('Trajectory Comparison (Top-Down View)', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_trajectory.py <kitti_file.txt>")
        print("       python plot_trajectory.py trajectory1.txt trajectory2.txt")
        print("Example: python plot_trajectory.py odom_kitti.txt")
        print("         python plot_trajectory.py odom_kitti.txt gt_kitti.txt")
        sys.exit(1)
    
    input_files = sys.argv[1:]
    
    # Check if files exist
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found!")
            sys.exit(1)
    
    if len(input_files) == 1:
        # Single trajectory
        positions, frame_ids = read_kitti_trajectory(input_files[0])
        print(f"Loaded {len(positions)} poses from {input_files[0]}")
        print(f"X range: {positions[:, 0].min():.3f} to {positions[:, 0].max():.3f}")
        print(f"Y range: {positions[:, 1].min():.3f} to {positions[:, 1].max():.3f}")
        plot_trajectory(positions, frame_ids, f"Trajectory: {os.path.basename(input_files[0])}")
    else:
        # Multiple trajectories
        plot_multiple_trajectories(input_files)