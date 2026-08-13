#!/usr/bin/env python3
"""
Interpolate planar ground-truth CSV (timestamp,x,y,phi,...) to per-frame KITTI poses.
Assumptions:
- CSV has a header and columns: timestamp,x,y,phi (or similar: --ts-col, --x-col, --y-col, --phi-col)
- Frames are in data/sequences_jpg/<seq>/image_<camera>/ and named %06d.jpg starting at 000000.jpg
- Default fps is 120. If video start time differs from first GT timestamp, pass --start-offset (seconds)

Example:
  python3 scripts/interpolate_gt_to_frames.py --sequence 30 --csv kitti/dataset/poses.csv/30.csv --fps 120

Options:
  --user-to-kitti : apply axis transform for your frame convention (X forward, Y left, Z up) -> KITTI
"""

import argparse
from pathlib import Path
import numpy as np
import csv


def read_csv_poses(path, ts_col=0, x_col=1, y_col=2, phi_col=3, has_header=True):
    rows = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        if has_header:
            next(reader, None)
        for r in reader:
            if not r: continue
            rows.append((float(r[ts_col]), float(r[x_col]), float(r[y_col]), float(r[phi_col])))
    arr = np.array(rows)
    return arr[:,0], arr[:,1], arr[:,2], arr[:,3]


def unwrap_angles(a):
    return np.unwrap(a)


def make_pose_from_xyphi(x, y, phi):
    c = np.cos(phi); s = np.sin(phi)
    R = np.array([[c, -s, 0.0],[s, c, 0.0],[0.0,0.0,1.0]])
    t = np.array([x, y, 0.0])
    return np.hstack([R, t.reshape(3,1)])


def user_to_kitti_matrix(m3x4):
    S = np.array([[0.0, -1.0, 0.0],[0.0,0.0,-1.0],[1.0,0.0,0.0]])
    R = m3x4[:,:3]
    t = m3x4[:,3]
    Rk = S @ R @ S.T
    tk = S @ t
    return np.hstack([Rk, tk.reshape(3,1)])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sequence','-q', required=True)
    p.add_argument('--csv', required=True)
    p.add_argument('--fps', type=float, default=120.0)
    p.add_argument('--camera', default='2')
    p.add_argument('--outdir', default='data/poses')
    p.add_argument('--frames-root', default='data/sequences_jpg')
    p.add_argument('--ts-col', type=int, default=0)
    p.add_argument('--x-col', type=int, default=1)
    p.add_argument('--y-col', type=int, default=2)
    p.add_argument('--phi-col', type=int, default=3)
    p.add_argument('--has-header', action='store_true')
    p.add_argument('--user-to-kitti', action='store_true')
    p.add_argument('--start-offset', type=float, default=0.0, help='seconds to add to frame times relative to first GT timestamp')
    args = p.parse_args()

    seq = args.sequence
    csvp = Path(args.csv)
    ts, xs, ys, phis = read_csv_poses(csvp, ts_col=args.ts_col, x_col=args.x_col, y_col=args.y_col, phi_col=args.phi_col, has_header=args.has_header)
    phis_un = unwrap_angles(phis)

    frames_dir = Path(args.frames_root) / seq / f"image_{args.camera}"
    if not frames_dir.exists():
        raise SystemExit(f"Frames folder not found: {frames_dir}")
    img_files = sorted(frames_dir.glob('*.jpg'))
    n_frames = len(img_files)
    if n_frames == 0:
        raise SystemExit('No frames found')

    # build frame timestamps: start at first GT ts + offset, step = 1/fps
    t0 = ts[0] + args.start_offset
    frame_ts = t0 + np.arange(n_frames) / args.fps

    # interpolate x,y and phi (on unwrapped angles)
    xi = np.interp(frame_ts, ts, xs)
    yi = np.interp(frame_ts, ts, ys)
    phii_un = np.interp(frame_ts, ts, phis_un)
    phii = ((phii_un + np.pi) % (2*np.pi)) - np.pi

    outp = Path(args.outdir)
    outp.mkdir(parents=True, exist_ok=True)
    with open(outp / f"{seq}.txt", 'w') as fo:
        for i in range(n_frames):
            m = make_pose_from_xyphi(xi[i], yi[i], phii[i])
            if args.user_to_kitti:
                m = user_to_kitti_matrix(m)
            fo.write(' '.join(f"{v:.6f}" for v in m.reshape(-1)) + '\n')

    print('Wrote', outp / f"{seq}.txt", 'for', n_frames, 'frames')

if __name__ == '__main__':
    main()
