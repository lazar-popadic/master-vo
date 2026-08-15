#!/usr/bin/env python3
"""
Reorient every GT pose file in results/TSformer-VO/gt_poses into the TSformer-VO
user convention:
  - x forward
  - y left
  - z up

This only updates the GT .txt files under the GT directory; the model prediction
files are left untouched.

The camera/KITTI convention used by the eval tool is converted back to the
TSformer-VO convention using the inverse of the user->KITTI transform:
  S = [[0, -1, 0],
       [0,  0, -1],
       [1,  0,  0]]
"""

from pathlib import Path
import numpy as np

GT_DIR = Path('/workspace/results/TSformer-VO/gt_poses')


def kitti_to_user_matrix(m3x4):
    """Convert a KITTI-frame 3x4 pose to the TSformer-VO user frame."""
    S = np.array([
        [0.0, -1.0, 0.0],
        [0.0, 0.0, -1.0],
        [1.0, 0.0, 0.0],
    ], dtype=np.float64)
    R = m3x4[:, :3]
    t = m3x4[:, 3]
    Ru = S.T @ R @ S
    tu = S.T @ t
    return np.hstack([Ru, tu.reshape(3, 1)])


def parse_pose_line(line):
    vals = line.strip().split()
    if not vals:
        return None

    if len(vals) == 13:
        vals = vals[1:]
    if len(vals) != 12:
        raise ValueError(f'Expected 12 pose values, got {len(vals)}: {line!r}')

    vals = [float(v) for v in vals]
    m = np.array(vals, dtype=np.float64).reshape(3, 4)
    return m


def write_pose_line(m, frame_idx=None):
    row = m.reshape(-1)
    vals = [f'{float(v):.12f}' for v in row]
    if frame_idx is not None:
        return ' '.join([str(int(frame_idx))] + vals)
    return ' '.join(vals)


def reorient_gt_file(gt_path: Path):
    lines = []
    with gt_path.open('r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = parse_pose_line(line)
            m_u = kitti_to_user_matrix(m)
            lines.append((len(lines), m_u))

    if not lines:
        print(f'SKIP empty file: {gt_path}')
        return

    with gt_path.open('w') as f:
        for frame_idx, m in lines:
            f.write(write_pose_line(m, frame_idx=frame_idx) + '\n')

    print(f'updated {gt_path} ({len(lines)} frames)')


if __name__ == '__main__':
    if not GT_DIR.exists():
        raise SystemExit(f'GT directory does not exist: {GT_DIR}')

    for gt_path in sorted(GT_DIR.glob('*.txt')):
        reorient_gt_file(gt_path)
