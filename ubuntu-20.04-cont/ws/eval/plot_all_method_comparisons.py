#!/usr/bin/env python3
"""Plot GT vs VO trajectories for the 4 GT trajectory families.

Each figure contains one GT trajectory and the matching aligned trajectories from
SVO, ORB-SLAM3, and TSformer-VO, as defined by the sequence mapping:

  curve_fast_gt    -> svo 00, orb 01, tsformer 30
  curve_slow_gt    -> svo 01, orb 03, tsformer 31
  straight_fast    -> svo 02, orb 05, tsformer 32
  straight_slow    -> svo 03, orb 07, tsformer 33
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GT_DIR = Path("/workspace/eval/gt")
RESULT_DIR = Path("/workspace/results")
OUTPUT_DIR = Path("/workspace/eval")

MAPPING = {
    "curve_fast": {
        "gt": "curve_sequence_v2_fast_gt.csv",
        "svo": "00",
        "orb": "01",
        "tsformer": "30",
    },
    "curve_slow": {
        "gt": "curve_sequence_v2_slow_gt.csv",
        "svo": "01",
        "orb": "03",
        "tsformer": "31",
    },
    "straight_fast": {
        "gt": "straight_sequence_v2_fast.csv",
        "svo": "02",
        "orb": "05",
        "tsformer": "32",
    },
    "straight_slow": {
        "gt": "straight_sequence_v2_slow.csv",
        "svo": "03",
        "orb": "07",
        "tsformer": "33",
    },
}


def read_gt_csv(path: Path) -> np.ndarray:
    positions = []
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            positions.append((float(row["x"]), float(row["y"])))
    return np.asarray(positions, dtype=float)


def read_aligned_pose_file(path: Path) -> np.ndarray:
    positions = []
    with path.open("r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) < 12:
                continue
            vals = parts[1:13] if len(parts) == 13 else parts[:12]
            try:
                pose = np.asarray([float(v) for v in vals], dtype=float).reshape(3, 4)
            except ValueError:
                continue
            positions.append(pose[:2, 3])
    return np.asarray(positions, dtype=float)


def get_method_path(method: str, seq_id: str) -> Path:
    if method == "svo":
        return RESULT_DIR / "svo" / "aligned" / f"{seq_id}.txt"
    if method == "orb":
        return RESULT_DIR / "orb" / "aligned" / f"{seq_id}.txt"
    if method == "tsformer":
        return RESULT_DIR / "TSformer-VO" / "Model3" / "aligned" / f"{seq_id}.txt"
    raise ValueError(f"Unknown method: {method}")


def plot_family(ax, name: str, mapping: dict, show_legend: bool = False):
    gt_path = GT_DIR / mapping["gt"]
    gt_points = read_gt_csv(gt_path)
    ax.plot(gt_points[:, 0], gt_points[:, 1], label="GT", color="k", linewidth=1.5, linestyle="--", alpha=0.9)

    method_styles = {
        "svo": ("tab:blue", "SVO"),
        "orb": ("tab:orange", "ORB-SLAM3"),
        "tsformer": ("tab:green", "TSformer-VO (Model 3)"),
    }

    for method, seq_id in [("svo", mapping["svo"]), ("orb", mapping["orb"]), ("tsformer", mapping["tsformer"])]:
        traj_path = get_method_path(method, seq_id)
        if not traj_path.exists():
            print(f"Missing file: {traj_path}")
            continue
        positions = read_aligned_pose_file(traj_path)
        color, label = method_styles[method]
        ax.plot(positions[:, 0], positions[:, 1], label=label, color=color, linewidth=1.2, alpha=0.9)

    title_map = {
        "curve_fast": "Sequence 2 - Fast",
        "curve_slow": "Sequence 2 - Slow",
        "straight_fast": "Sequence 1 - Fast",
        "straight_slow": "Sequence 1 - Slow",
    }
    ax.set_title(title_map.get(name, name.replace("_", " ").title()), fontsize=11, fontweight="bold")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.grid(True, alpha=0.3)
    ax.axis("equal")

    if show_legend:
        ax.legend(loc="upper right", frameon=True)


def main():
    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    axis_list = axes.flatten()

    for ax, (family_name, family_mapping) in zip(axis_list, MAPPING.items()):
        plot_family(ax, family_name, family_mapping, show_legend=(ax is axes[0, 1]))

    fig.tight_layout()
    out_path = OUTPUT_DIR / "all_sequences_2x2.png"
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved: {out_path}")

    for family_name, family_mapping in MAPPING.items():
        fig, ax = plt.subplots(figsize=(8, 8))
        plot_family(ax, family_name, family_mapping, show_legend=True)
        output_name_map = {
            "curve_fast": "sequence_2_fast.png",
            "curve_slow": "sequence_2_slow.png",
            "straight_fast": "sequence_1_fast.png",
            "straight_slow": "sequence_1_slow.png",
        }
        out_file = OUTPUT_DIR / output_name_map[family_name]
        plt.tight_layout()
        fig.savefig(out_file, dpi=200)
        plt.close(fig)
        print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
