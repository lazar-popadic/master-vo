#!/usr/bin/env python3
from pathlib import Path
import numpy as np

def read_pose_file(p):
    d = np.loadtxt(p)
    if d.ndim == 1:
        d = d.reshape(1, -1)
    return d


def build_svg(tx, tz, w=800, h=800, margin=20):
    sx = tx - tx.min()
    sz = tz - tz.min()
    rngx = sx.max() if sx.max()>0 else 1.0
    rngz = sz.max() if sz.max()>0 else 1.0
    pts = []
    for x,y in zip(sx, sz):
        px = margin + (w-2*margin) * (x / rngx)
        py = margin + (h-2*margin) * (y / rngz)
        pts.append(f"{px:.1f},{h-py:.1f}")
    poly = ' '.join(pts)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
    svg += f'<polyline points="{poly}" fill="none" stroke="black" stroke-width="1" />'
    if pts:
        svg += f'<circle cx="{pts[0].split(",")[0]}" cy="{pts[0].split(",")[1]}" r="4" fill="green" />'
        svg += f'<circle cx="{pts[-1].split(",")[0]}" cy="{pts[-1].split(",")[1]}" r="4" fill="red" />'
    svg += '</svg>'
    return svg


def plot_seq(seq, poses_dir, out_dir):
    p = Path(poses_dir) / f"{seq}.txt"
    if not p.exists():
        print('missing', p)
        return None
    d = read_pose_file(str(p))
    tx = d[:,3]
    tz = d[:,11]
    # compute yaw as atan2(r13, r33) where r13 index 2, r33 index 10
    r13 = d[:,2]
    r33 = d[:,10]
    yaw = np.arctan2(r13, r33)
    svg = build_svg(tx, tz)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    outf = out / f'seq_{seq}.svg'
    outf.write_text(svg)
    # also write small yaw plot as CSV for visual check
    yawf = out / f'seq_{seq}_yaw.csv'
    np.savetxt(yawf, yaw)
    return outf

if __name__ == '__main__':
    import sys
    seqs = sys.argv[1].split(',') if len(sys.argv)>1 else ['30','31','32','33']
    poses_dir = sys.argv[2] if len(sys.argv)>2 else 'data/poses'
    out_dir = sys.argv[3] if len(sys.argv)>3 else 'kitti/dataset/pose_plots'
    for s in seqs:
        out = plot_seq(s, poses_dir, out_dir)
        if out:
            print('Wrote', out)
