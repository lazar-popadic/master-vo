#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load trajectory
traj = np.loadtxt('/workspace/orb_slam_visualization/V2/straight_sequence_v2_slow_kf_traj.txt')

# Extract positions
positions = traj[:, 1:4]
timestamps = traj[:, 0]

# Detect reinitialization by large position jumps
distances = np.linalg.norm(np.diff(positions, axis=0), axis=1)
mean_dist = np.mean(distances)
std_dist = np.std(distances)
threshold = mean_dist + 3 * std_dist

# Find reset points
reset_indices = np.where(distances > threshold)[0] + 1
reset_indices = np.insert(reset_indices, 0, 0)
reset_indices = np.append(reset_indices, len(positions))

print(f"Found {len(reset_indices)-1} continuous tracking segments\n")

# Extract and visualize segments
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

colors = plt.cm.tab10(np.linspace(0, 1, len(reset_indices)-1))

for i in range(len(reset_indices) - 1):
    start_idx = reset_indices[i]
    end_idx = reset_indices[i+1]
    
    segment = positions[start_idx:end_idx]
    segment_times = timestamps[start_idx:end_idx]
    duration = segment_times[-1] - segment_times[0] if len(segment_times) > 1 else 0
    
    print(f"Segment {i}: {len(segment)} frames, duration: {duration:.2f}s")
    
    # Plot segment
    ax.plot(segment[:, 0], segment[:, 1], segment[:, 2], 
            color=colors[i], linewidth=2, label=f'Segment {i} ({len(segment)} frames)')
    
    # Mark start and end
    ax.scatter(segment[0, 0], segment[0, 1], segment[0, 2], 
              color=colors[i], s=50, marker='o')
    ax.scatter(segment[-1, 0], segment[-1, 1], segment[-1, 2], 
              color=colors[i], s=50, marker='x')

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.legend(loc='upper left', fontsize=8)
ax.set_title('ORB-SLAM3 Tracked Segments (Continuous Tracking Periods)')
plt.tight_layout()
plt.savefig('/workspace/trajectory_segments.png', dpi=150)
print(f"\nVisualization saved to /workspace/trajectory_segments.png")
plt.show()
