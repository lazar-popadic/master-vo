#!/usr/bin/env python3
"""Compute cumulative trajectory lengths from the pose files in /workspace/results."""

from pathlib import Path

import numpy as np

RESULT_ROOT = Path("/workspace/results")
EXCLUDED_DIRS = {
    "aligned_plots",
    "errors",
    "gt_poses",
    "plot_error",
    "plot_path",
    "scaled",
    "scaled_then_6dof_aligned",
    "original",
    "just ran with ai budz",
    "aligned and again",
    "aligned again with ai budz",
}


def parse_pose_row(line: str):
    """Return (3,4) pose matrix from a KITTI-style line."""
    parts = line.strip().split()
    if len(parts) < 12:
        return None

    if len(parts) == 13:
        vals = parts[1:13]
    else:
        vals = parts[:12]

    try:
        return np.asarray([float(v) for v in vals], dtype=float).reshape(3, 4)
    except ValueError:
        return None


def read_positions_from_file(file_path: Path):
    """Read the x/y translation of each pose in a file."""
    positions = []

    with file_path.open("r") as f:
        for line in f:
            if not line.strip():
                continue
            pose = parse_pose_row(line)
            if pose is not None:
                positions.append(pose[:2, 3])

    return np.asarray(positions, dtype=float)


def trajectory_length(points: np.ndarray) -> float:
    if points.size == 0 or len(points) < 2:
        return 0.0
    deltas = np.diff(points, axis=0)
    segment_lengths = np.linalg.norm(deltas, axis=1)
    return float(segment_lengths.sum())


def main():
    files = []
    for path in sorted(RESULT_ROOT.rglob("*.txt")):
        if path.name in {"result.txt", "seq_lengths.txt"}:
            continue

        if path.parent.name != "aligned":
            continue

        rel_parts = path.relative_to(RESULT_ROOT).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts[:-1]):
            continue
        files.append(path)

    if not files:
        print(f"No aligned trajectory pose files found in {RESULT_ROOT}")
        return

    total = 0.0
    print(f"Calculated aligned trajectory lengths in {RESULT_ROOT}:")
    for file_path in files:
        positions = read_positions_from_file(file_path)
        length = trajectory_length(positions)
        total += length
        print(f"{file_path.relative_to(RESULT_ROOT)}: {length:.3f} m")

    print(f"TOTAL: {total:.3f} m")


if __name__ == "__main__":
    main()
