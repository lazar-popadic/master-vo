#!/usr/bin/env python3
"""Convert predicted poses (.npy) to KITTI-format 3x4 TXT and optionally plot sequence 02.

Usage examples:
  python3 scripts/convert_preds_to_kitti_and_plot.py --pred-dir TSformer-VO/models/Model3/checkpoint_model3_exp20 \
    --args-pkl TSformer-VO/models/Model3/args.pkl --sequences 02,30,31,32,33 --out-dir TSformer-VO/models/Model3/checkpoint_model3_exp20 --plot 02
"""
import argparse
import os
import pickle
import numpy as np
import math
import functools
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def euler_to_rotation(z=0, y=0, x=0, isRadian=True, seq='zyx'):
    import numpy as _np
    if not isRadian:
        z = (math.pi / 180.0) * z
        y = (math.pi / 180.0) * y
        x = (math.pi / 180.0) * x
    Ms = []
    if seq == 'zyx':
        if abs(z) > 0:
            cosz = math.cos(z); sinz = math.sin(z)
            Ms.append(_np.array([[cosz, -sinz, 0],[sinz, cosz, 0],[0,0,1]]))
        if abs(y) > 0:
            cosy = math.cos(y); siny = math.sin(y)
            Ms.append(_np.array([[cosy, 0, siny],[0,1,0],[-siny,0,cosy]]))
        if abs(x) > 0:
            cosx = math.cos(x); sinx = math.sin(x)
            Ms.append(_np.array([[1,0,0],[0,cosx,-sinx],[0,sinx,cosx]]))
        if Ms:
            return functools.reduce(_np.dot, Ms[::-1])
        return _np.eye(3)
    else:
        raise Exception('Sequence not recognized')


def convert_preds_to_kitti(pred_npy, args_pkl, out_txt):
    # Load preds
    preds = np.load(pred_npy)

    # Load args to obtain window params (fallbacks if missing)
    if os.path.exists(args_pkl):
        with open(args_pkl, 'rb') as f:
            args = pickle.load(f)
        S = args.get('window_size', 4)
        overlap = args.get('overlap', 3)
    else:
        S = 4
        overlap = 3

    W = preds.shape[0]
    step = S - overlap
    # infer frame counts
    N = (W - 1) * step + S
    M = N - 1

    # average overlapping transition predictions
    trans = np.zeros((M, 6), dtype=float)
    counts = np.zeros((M,), dtype=int)
    for i in range(W):
        start = i * step
        for k in range(S-1):
            idx = start + k
            if idx < M:
                trans[idx] += preds[i, k]
                counts[idx] += 1
    mask = counts > 0
    trans[mask] = trans[mask] / counts[mask][:, None]

    # denormalize using KITTI stats (matches dataset implementation)
    mean_angles = np.array([1.7061e-5, 9.5582e-4, -5.5258e-5])
    std_angles = np.array([2.8256e-3, 1.7771e-2, 3.2326e-3])
    mean_t = np.array([-8.6736e-5, -1.6038e-2, 9.0033e-1])
    std_t = np.array([2.5584e-2, 1.8545e-2, 3.0352e-1])

    angles = trans[:, :3] * std_angles + mean_angles
    tvecs = trans[:, 3:6] * std_t + mean_t

    # build absolute poses from relative transitions
    poses = []
    T = np.eye(4)
    poses.append(T[:3, :4].copy())
    for i in range(M):
        z, y, x = angles[i]
        R = euler_to_rotation(z, y, x, True, 'zyx')
        t = tvecs[i]
        T_rel = np.eye(4)
        T_rel[:3, :3] = R
        T_rel[:3, 3] = t
        T = T @ T_rel
        poses.append(T[:3, :4].copy())

    # write out
    os.makedirs(os.path.dirname(out_txt), exist_ok=True)
    with open(out_txt, 'w') as f:
        for p in poses:
            row = p.reshape(-1)
            f.write(' '.join(['{:.12f}'.format(float(x)) for x in row]) + '\n')

    return out_txt, len(poses)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pred-dir', default='TSformer-VO/models/Model3/checkpoint_model3_exp20', help='Directory with pred_poses_<seq>.npy')
    p.add_argument('--args-pkl', default='TSformer-VO/models/Model3/args.pkl', help='Path to args.pkl for window params')
    p.add_argument('--sequences', default='30,31,32,33', help='Comma-separated sequence ids')
    p.add_argument('--out-dir', default=None, help='Output dir for KITTI txt files (defaults to pred-dir)')
    p.add_argument('--plot', default=None, help='Sequence id to plot after conversion (e.g. 02)')
    p.add_argument('--move-to-data', action='store_true', help='Also copy written TXT into data/poses/<seq>.txt')
    args = p.parse_args()

    pred_dir = args.pred_dir
    out_root = args.out_dir or pred_dir
    seqs = [s.strip() for s in args.sequences.split(',') if s.strip()]

    written = []
    for seq in seqs:
        npy = os.path.join(pred_dir, f'pred_poses_{seq}.npy')
        out_txt = os.path.join(out_root, f'pred_poses_{seq}_kitti.txt')
        if not os.path.exists(npy):
            print('Missing prediction:', npy)
            continue
        out, nlines = convert_preds_to_kitti(npy, args.args_pkl, out_txt)
        print(f'Wrote {out} ({nlines} lines)')
        written.append((seq, out))
        if args.move_to_data:
            dst = os.path.join('data', 'poses', f'{seq}.txt')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(out, 'r') as r, open(dst, 'w') as w:
                w.write(r.read())
            print('Copied to', dst)

    # plot requested sequence directly to PNG using matplotlib (no SVG)
    if args.plot:
        plot_seq = args.plot
        poses_dir = 'data/poses' if args.move_to_data else out_root
        plot_out = os.path.join('kitti', 'dataset', 'pose_plots')
        os.makedirs(plot_out, exist_ok=True)

        pose_file = os.path.join(poses_dir, f'{plot_seq}.txt')
        if not os.path.exists(pose_file):
            print('Missing pose file for plotting:', pose_file)
        else:
            data = np.loadtxt(pose_file)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            tx = data[:, 3]
            tz = data[:, 11]
            plt.figure(figsize=(8, 8))
            plt.plot(tx, tz, '-k', linewidth=1)
            plt.scatter([tx[0]], [tz[0]], c='g', s=40, label='start')
            plt.scatter([tx[-1]], [tz[-1]], c='r', s=40, label='end')
            plt.title(f'Sequence {plot_seq}')
            plt.xlabel('tx')
            plt.ylabel('tz')
            plt.legend()
            png_path = os.path.join(plot_out, f'seq_{plot_seq}.png')
            plt.tight_layout()
            plt.savefig(png_path)
            plt.close()
            print('Wrote PNG:', png_path)


if __name__ == '__main__':
    main()
