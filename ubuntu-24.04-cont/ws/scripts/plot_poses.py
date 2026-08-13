#!/usr/bin/env python3
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read_pose_file(p):
    data = np.loadtxt(p)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    # tx = col 3, ty = col 7, tz = col 11
    tx = data[:, 3]
    ty = data[:, 7]
    tz = data[:, 11]
    # yaw from R: atan2(r21, r11) => r21=data[:,4], r11=data[:,0]
    yaw = np.arctan2(data[:, 4], data[:, 0])
    return tx, ty, tz, yaw


def plot_sequence(seq, pose_path, out_dir):
    tx, ty, tz, yaw = read_pose_file(pose_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, axs = plt.subplots(1,2, figsize=(10,4))
    # top-down: X (tx) vs Z (tz)
    axs[0].plot(tx, tz, '-k')
    axs[0].plot(tx[0], tz[0], 'go', label='start')
    axs[0].plot(tx[-1], tz[-1], 'ro', label='end')
    axs[0].set_xlabel('tx (m)')
    axs[0].set_ylabel('tz (m)')
    axs[0].set_title(f'Sequence {seq} top-down')
    axs[0].legend()
    # yaw over frames
    axs[1].plot(np.arange(len(yaw)), np.unwrap(yaw), '-b')
    axs[1].set_xlabel('frame')
    axs[1].set_ylabel('yaw (rad)')
    axs[1].set_title(f'Sequence {seq} yaw')
    plt.tight_layout()
    out_file = out_dir / f'seq_{seq}.png'
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    return out_file


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sequences', default='30,31,32,33')
    p.add_argument('--poses-dir', default='data/poses')
    p.add_argument('--out-dir', default='result/pose_plots')
    args = p.parse_args()
    seqs = [s.strip() for s in args.sequences.split(',') if s.strip()]
    poses_root = Path(args.poses_dir)
    out_root = Path(args.out_dir)
    created = []
    for s in seqs:
        pose_file = poses_root / f"{s}.txt"
        if not pose_file.exists():
            print('Missing pose file', pose_file)
            continue
        out = plot_sequence(s, pose_file, out_root)
        print('Wrote', out)
        created.append(out)
    if not created:
        print('No plots created')

if __name__ == '__main__':
    main()
