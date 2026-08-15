#!/usr/bin/env python3

import csv
from pathlib import Path

ROOT = Path('/workspace/results/TSformer-VO')
MODELS = ['Model1', 'Model2', 'Model3']
GT_DIR = Path('/workspace/results/TSformer-VO/gt_poses')


def load_gt_count(gt_path: Path) -> int:
    with gt_path.open('r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return len(lines)


def parse_pose_line(line):
    vals = line.strip().split()
    if not vals:
        return []
    if len(vals) == 13:
        vals = vals[1:]
    if len(vals) != 12:
        raise ValueError(f'Expected 12 pose values, got {len(vals)}: {line!r}')
    return vals


def add_frame_index_to_gt(gt_path: Path) -> None:
    with gt_path.open('r') as f:
        lines = [line.strip() for line in f if line.strip()]

    indexed_lines = []
    for idx, line in enumerate(lines):
        vals = line.split()
        if len(vals) == 12:
            indexed_lines.append(f'{idx} ' + ' '.join(vals))
        elif len(vals) == 13:
            indexed_lines.append(f'{idx} ' + ' '.join(vals[1:]))
        else:
            raise ValueError(f'Unexpected GT row length for {gt_path}: {len(vals)}')

    with gt_path.open('w') as out:
        for line in indexed_lines:
            out.write(line + '\n')

    print(f'{gt_path}: wrote {len(indexed_lines)} indexed GT frames')


def trim_and_write(model_dir: Path) -> None:
    for pred_path in sorted(model_dir.glob('*.txt')):
        seq_id = pred_path.stem
        gt_path = GT_DIR / f'{seq_id}.txt'
        if not gt_path.exists():
            print(f'SKIP {pred_path}: no GT file at {gt_path}')
            continue

        add_frame_index_to_gt(gt_path)

        with pred_path.open('r') as f:
            pose_lines = [parse_pose_line(line) for line in f if line.strip()]

        gt_count = load_gt_count(gt_path)
        if gt_count <= 0:
            print(f'SKIP {pred_path}: GT file empty')
            continue

        trimmed = pose_lines[:gt_count]
        if len(trimmed) < gt_count:
            print(f'WARN {pred_path}: predicted frames={len(pose_lines)} < GT frames={gt_count}; writing {len(trimmed)} frames')

        with pred_path.open('w') as out:
            for idx, vals in enumerate(trimmed):
                out.write(f'{idx} ' + ' '.join(vals) + '\n')

        print(f'{pred_path}: wrote {len(trimmed)} frames (GT={gt_count})')


if __name__ == '__main__':
    for model in MODELS:
        model_dir = ROOT / model
        if not model_dir.exists():
            print(f'SKIP model dir {model_dir}: missing')
            continue
        trim_and_write(model_dir)
