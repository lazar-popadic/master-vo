#!/usr/bin/env python3
"""
Convert CSV pose files into KITTI odometry pose format (data/poses/<seq>.txt).

Supported input row types:
- 12 numbers: first 12 values are the 3x4 pose row-major -> copied directly
- 16 numbers: 4x4 pose matrix row-major -> first 3 rows x 4 columns used
- 6 numbers: rotation (Euler) + translation. Use --angles-order to specify order.
  Example orders: 'zyx' (yaw,pitch,roll), 'xyz' (roll,pitch,yaw). Default is 'zyx'.

Usage examples:
  # 12-values per row -> write poses for sequence 30
  python3 scripts/csv_to_kitti_poses.py --input poses.csv --sequence 30 --outdir data/poses --format row12

  # 6-values per row, columns 0..5 are angles (deg) then tx,ty,tz, angles in degrees, order zyx
  python3 scripts/csv_to_kitti_poses.py --input poses.csv --sequence 30 --outdir data/poses --format euler6 --cols 0,1,2,3,4,5 --angles-order zyx --deg

  # If the CSV has a header, use --has-header

If you're not sure about the CSV layout, send me a few lines (head) and I'll pick options for you.
"""

import argparse
from pathlib import Path
import numpy as np
import csv


def euler_to_rot_matrix(angles, order='zyx'):
    # angles: iterable of three angles [a0,a1,a2] corresponding to order
    a = dict(zip(order, angles))
    # build individual rotation matrices
    def Rx(t):
        return np.array([[1,0,0],[0,np.cos(t),-np.sin(t)],[0,np.sin(t),np.cos(t)]])
    def Ry(t):
        return np.array([[np.cos(t),0,np.sin(t)],[0,1,0],[-np.sin(t),0,np.cos(t)]])
    def Rz(t):
        return np.array([[np.cos(t),-np.sin(t),0],[np.sin(t),np.cos(t),0],[0,0,1]])
    R = np.eye(3)
    # apply in order: first rotation around order[0], then order[1], then order[2]
    for axis in order:
        if axis == 'x': R = R @ Rx(a[axis])
        if axis == 'y': R = R @ Ry(a[axis])
        if axis == 'z': R = R @ Rz(a[axis])
    return R


def row_to_pose_line(row_vals, fmt, angles_order='zyx', degrees=False):
    vals = [float(x) for x in row_vals]
    if fmt == 'row12':
        # take first 12 values
        vals12 = vals[:12]
        return np.array(vals12, dtype=float)
    if fmt == 'row16':
        vals16 = vals[:16]
        # take first 3 rows x 4 cols
        m = np.array(vals16).reshape((4,4))
        m3x4 = m[:3,:4].reshape(-1)
        return m3x4.astype(float)
    if fmt == 'euler6':
        # expects 6 values: angles (3) then translation (3)
        angles = vals[:3]
        t = vals[3:6]
        if degrees:
            angles = [np.deg2rad(a) for a in angles]
        R = euler_to_rot_matrix(angles, order=angles_order)
        m3x4 = np.hstack([R, np.array(t).reshape(3,1)])
        return m3x4.reshape(-1).astype(float)
    raise ValueError('Unsupported format')


def detect_and_convert(input_csv, out_path, fmt, cols, angles_order, degrees, has_header, user_to_kitti=False):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(input_csv, 'r') as f_in, open(out_path, 'w') as f_out:
        reader = csv.reader(f_in)
        if has_header:
            next(reader, None)
        for row in reader:
            if not row:
                continue
            # select columns if requested
            if cols is not None:
                row_sel = [row[i] for i in cols]
            else:
                row_sel = row
            # convert to numeric 12-element pose (3x4 row-major)
            if fmt in ('planar_xyphi', 'planar_xyphivw'):
                try:
                    x = float(row_sel[1])
                    y = float(row_sel[2])
                    phi = float(row_sel[3])
                except Exception:
                    raise ValueError(f'Row does not match planar format: {row_sel}')
                c = np.cos(phi)
                s = np.sin(phi)
                R = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
                t = np.array([x, 0.0, y])
                m_vals = np.hstack([R, t.reshape(3,1)]).reshape(-1)
            else:
                m_vals = row_to_pose_line(row_sel, fmt, angles_order, degrees)

            # apply user->KITTI axis transform if requested
            if user_to_kitti:
                S = np.array([[0.0, -1.0, 0.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0]])
                m = m_vals.reshape(3,4)
                R_user = m[:, :3]
                t_user = m[:, 3]
                R_k = S @ R_user @ S.T
                t_k = S @ t_user
                m_k = np.hstack([R_k, t_k.reshape(3,1)])
                m_vals = m_k.reshape(-1)

            line = ' '.join(f"{v:.6f}" for v in m_vals)
            f_out.write(line + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='Input CSV file')
    parser.add_argument('--sequence', '-q', required=True, help='Sequence id to write (e.g. 30)')
    parser.add_argument('--outdir', '-o', default='data/poses', help='Output directory for KITTI poses')
    parser.add_argument('--format', choices=['row12','row16','euler6','planar_xyphi','planar_xyphivw'], default='row12', help='Format of CSV rows')
    parser.add_argument('--cols', help='Comma-separated column indices to use (0-based), e.g. 0,1,2,3,4,5')
    parser.add_argument('--angles-order', default='zyx', help="Order of Euler angles, e.g. 'zyx' or 'xyz' (default zyx)")
    parser.add_argument('--deg', action='store_true', help='Angles are in degrees')
    parser.add_argument('--has-header', action='store_true', help='CSV has a header row')
    parser.add_argument('--user-to-kitti', action='store_true', help='Apply axis transform from user frame (X-forward,Y-left,Z-up) to KITTI frame')
    args = parser.parse_args()

    cols = None
    if args.cols:
        cols = [int(x) for x in args.cols.split(',')]

    input_csv = Path(args.input)
    seq = args.sequence
    outdir = Path(args.outdir)
    out_path = outdir / f"{seq}.txt"

    detect_and_convert(input_csv, out_path, args.format, cols, args.angles_order, args.deg, args.has_header, user_to_kitti=args.user_to_kitti)
    print('Wrote', out_path)

if __name__ == '__main__':
    main()
