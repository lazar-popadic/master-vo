"""Example of pykitti.odometry usage."""
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time
from mpl_toolkits.mplot3d import Axes3D

import pykitti

__author__ = "Lee Clement"
__email__ = "lee.clement@robotics.utias.utoronto.ca"

basedir = '/workspace/kitti/dataset'

# Specify the dataset to load
sequence = '09'

# Load the data. Optionally, specify the frame range to load.
temp = pykitti.odometry(basedir, sequence)
dataset = pykitti.odometry(basedir, sequence, frames=range(0, len(temp.timestamps), 10))
# dataset = pykitti.odometry(basedir, sequence, frames=range(0, 50, 5))

# dataset.calib:      Calibration data are accessible as a named tuple
# dataset.timestamps: Timestamps are parsed into a list of timedelta objects
# dataset.poses:      List of ground truth poses T_w_cam0
# dataset.camN:       Generator to load individual images from camera N
# dataset.gray:       Generator to load monochrome stereo pairs (cam0, cam1)
# dataset.rgb:        Generator to load RGB stereo pairs (cam2, cam3)
# dataset.velo:       Generator to load velodyne scans as [x,y,z,reflectance]

# Grab some data
second_pose = dataset.poses[1]
first_gray = next(iter(dataset.gray))
first_cam1 = next(iter(dataset.cam1))

# Display some of the data
np.set_printoptions(precision=4, suppress=True)
print('\nSequence: ' + str(dataset.sequence))
print('\nFrame range: ' + str(dataset.frames))
# print('\nGray stereo pair baseline [m]: ' + str(dataset.calib.b_gray))

# f, ax = plt.subplots(2, 2, figsize=(15, 5))
# ax[0, 0].imshow(first_gray[0], cmap='gray')
# ax[0, 0].set_title('Left Gray Image (cam0)')

# ax[0, 1].imshow(first_cam1, cmap='gray')
# ax[0, 1].set_title('Right Gray Image (cam1)')

# f2 = plt.figure()
# ax2 = f2.add_subplot(111, projection='3d')

# Initialize outside the loop
plt.ion()
fig = plt.figure(figsize=(15, 5))
fig.canvas.draw_idle()

# Create all subplots once
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2)
ax3 = plt.subplot(1, 3, 3)

# Initialize trajectory line
trajectory = []
line, = ax3.plot([], [], 'b-', linewidth=1)
point = ax3.scatter([], [], c='r', s=50)

ax3.set_xlabel('X')
ax3.set_ylabel('Z')
ax3.set_title('Camera Trajectory (Top-down)')
ax3.grid(True)
ax3.axis('equal')

for idx, frame_idx in enumerate(dataset.frames):
    left_img = dataset.get_cam0(idx)
    right_img = dataset.get_cam1(idx)
    
    # Update pose
    pose = dataset.poses[idx]
    trajectory.append([pose[0,3], pose[2,3]])
    trajectory_np = np.array(trajectory)
    
    # Update images
    ax1.clear()
    ax1.imshow(left_img, cmap='gray')
    ax1.set_title(f'Frame {frame_idx} - Left')
    ax1.axis('off')
    
    ax2.clear()
    ax2.imshow(right_img, cmap='gray')
    ax2.set_title(f'Frame {frame_idx} - Right')
    ax2.axis('off')
    
    # Update trajectory
    line.set_data(trajectory_np[:,0], trajectory_np[:,1])
    point.set_offsets([trajectory_np[-1,0], trajectory_np[-1,1]])
    
    # Adjust limits if needed
    ax3.relim()
    ax3.autoscale_view()
    
    plt.tight_layout()
    # plt.draw()
    # plt.pause(0.0001)
    fig.canvas.flush_events()

plt.show(block=True)