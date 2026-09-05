#!/usr/bin/env python3
"""
Plot all ground truth trajectories from /workspace/eval/gt/ directory
Displays all 4 trajectories on a single plot for comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
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
    
    # Plot only the requested trajectories.
    requested_files = [
        "curve_sequence_v2_fast_gt.csv",
        "straight_sequence_v2_slow.csv",
    ]
    csv_files = [gt_dir / file_name for file_name in requested_files]
    
    if not csv_files:
        print(f"No CSV files found in {gt_dir}")
        return
    
    print(f"Found {len(csv_files)} trajectory files:")
    for f in csv_files:
        print(f"  - {f.name}")
    
    # Plot each trajectory in a separate figure
    for file_path in csv_files:
        label = file_path.stem  # filename without extension
        if not file_path.exists():
            print(f"Warning: {file_path} does not exist")
            continue

        positions = read_csv_trajectory(file_path)
        
        if len(positions) == 0:
            print(f"Warning: {label} has no data")
            continue
        
        # Create a new figure for this trajectory
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot trajectory line
        ax.plot(positions[:, 0], positions[:, 1], color='black', linewidth=2.5)
        
        # Set axis limits
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 2)
        
        ax.grid(True, alpha=0.3)
        
        print(f"{label}: {len(positions)} points, "
              f"start=({positions[0, 0]:.3f}, {positions[0, 1]:.3f}), "
              f"end=({positions[-1, 0]:.3f}, {positions[-1, 1]:.3f})")
        
        # Save as PNG
        output_path = Path("/workspace/eval") / f"{label}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {output_path}")

        # Save vector versions for lossless paper scaling.
        svg_path = Path("/workspace/eval") / f"{label}.svg"
        pdf_path = Path("/workspace/eval") / f"{label}.pdf"
        plt.savefig(svg_path, bbox_inches='tight')
        plt.savefig(pdf_path, bbox_inches='tight')
        print(f"Saved to {svg_path}")
        print(f"Saved to {pdf_path}")
        plt.close()

if __name__ == "__main__":
    main()
