#!/usr/bin/env python3
"""
Plot all ground truth trajectories from /workspace/eval/gt/ directory
Displays all 4 trajectories on a single plot for comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from pathlib import Path

def read_csv_trajectory(file_path):
    """
    Read CSV trajectory file with columns: timestamp, x, y, phi_unmodified
    Returns: array of (x, y) positions
    """
    positions = []
    
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row['x'])
            y = float(row['y'])
            positions.append((x, y))
    
    return np.array(positions)

def main():
    # Directory containing ground truth trajectories
    gt_dir = Path("/workspace/eval/gt/")
    
    # Find all CSV files
    csv_files = sorted(list(gt_dir.glob("*.csv")))
    
    if not csv_files:
        print(f"No CSV files found in {gt_dir}")
        return
    
    print(f"Found {len(csv_files)} trajectory files:")
    for f in csv_files:
        print(f"  - {f.name}")
    
    # Colors for trajectories
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    # Plot each trajectory in a separate figure
    for idx, file_path in enumerate(csv_files):
        label = file_path.stem  # filename without extension
        positions = read_csv_trajectory(file_path)
        
        if len(positions) == 0:
            print(f"Warning: {label} has no data")
            continue
        
        color = colors[idx % len(colors)]
        
        # Create a new figure for this trajectory
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot trajectory line
        ax.plot(positions[:, 0], positions[:, 1], linewidth=2.5)
        
        # Set axis limits
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 2)
        
        # Labels and formatting
        ax.set_xlabel('X (meters)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y (meters)', fontsize=12, fontweight='bold')
        ax.set_title(f'{label}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        print(f"{label}: {len(positions)} points, "
              f"start=({positions[0, 0]:.3f}, {positions[0, 1]:.3f}), "
              f"end=({positions[-1, 0]:.3f}, {positions[-1, 1]:.3f})")
        
        # Save as PNG
        output_path = gt_dir / f"{label}.png"
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        print(f"Saved to {output_path}")
        plt.close()

if __name__ == "__main__":
    main()
