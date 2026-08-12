cd /workspace && python3 - <<'PY'
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load_poses(path):
    poses = {}
    with open(path, 'r') as f:
        for cnt, line in enumerate(f):
            tokens = [t for t in line.strip().split() if t!='']
            if not tokens:
                continue
            vals = [float(x) for x in tokens]
            has_idx = len(vals) == 13
            if has_idx:
                idx = int(vals[0])
                vals = vals[1:]
            else:
                idx = cnt
            P = np.eye(4)
            for row in range(3):
                for col in range(4):
                    P[row, col] = vals[row*4 + col]
            poses[idx] = P
    return poses

base = 'kitti-odom-eval/result'
for dataset in ['orb', 'svo']:
    gt_dir = os.path.join(base, dataset, 'gt_poses')
    aligned_dir = os.path.join(base, dataset, 'aligned')
    out_dir = os.path.join(base, dataset, 'aligned_plots')
    os.makedirs(out_dir, exist_ok=True)
    fname = '03.txt'
    aligned_path = os.path.join(aligned_dir, fname)
    gt_path = os.path.join(gt_dir, fname)
    if not os.path.exists(aligned_path):
        raise FileNotFoundError(aligned_path)
    if not os.path.exists(gt_path):
        raise FileNotFoundError(gt_path)
    aligned = load_poses(aligned_path)
    gt = load_poses(gt_path)
    common = sorted(set(aligned.keys()) & set(gt.keys()))
    if not common:
        raise ValueError('No common frames for %s' % dataset)
    aligned_xy = np.array([[aligned[i][0,3], aligned[i][1,3]] for i in common])
    gt_xy = np.array([[gt[i][0,3], gt[i][1,3]] for i in common])
    plt.figure(figsize=(8,8))
    plt.plot(gt_xy[:,0], gt_xy[:,1], label='GT', linewidth=2)
    plt.plot(aligned_xy[:,0], aligned_xy[:,1], label='Aligned', linewidth=2)
    plt.axis('equal')
    plt.title(f'{dataset.upper()} sequence 03')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.legend()
    plt.grid(True)
    out_path = os.path.join(out_dir, '03.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=200)
    plt.close()
    print('wrote', out_path)
PY