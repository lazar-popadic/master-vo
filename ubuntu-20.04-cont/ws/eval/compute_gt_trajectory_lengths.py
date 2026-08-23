#!/usr/bin/env python3
"""Compute the path length of each ground-truth trajectory in /workspace/eval/gt."""

import csv
from pathlib import Path

import numpy as np


def read_positions(csv_path: Path) -> np.ndarray:
    """Read x/y positions from a CSV trajectory file."""
    positions = []

    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)

        if "x" not in reader.fieldnames or "y" not in reader.fieldnames:
            raise ValueError(f"{csv_path} does not contain x and y columns")

        for row in reader:
            positions.append((float(row["x"]), float(row["y"])))

    return np.asarray(positions, dtype=float)


def trajectory_length(points: np.ndarray) -> float:
    """Compute the cumulative Euclidean distance along a trajectory."""
    if points.size == 0:
        return 0.0
    if len(points) < 2:
        return 0.0

    deltas = np.diff(points, axis=0)
    segment_lengths = np.linalg.norm(deltas, axis=1)
    return float(segment_lengths.sum())


def main() -> None:
    gt_dir = Path("/workspace/eval/gt")
    csv_files = sorted(gt_dir.glob("*.csv"))

    if not csv_files:
        print(f"No trajectory CSV files found in {gt_dir}")
        return

    total_length = 0.0
    print(f"Trajectory lengths in {gt_dir}:")

    for csv_path in csv_files:
        positions = read_positions(csv_path)
        length = trajectory_length(positions)
        total_length += length
        print(f"{csv_path.name}: {length:.3f} m")

    print(f"Total: {total_length:.3f} m")


if __name__ == "__main__":
    main()
