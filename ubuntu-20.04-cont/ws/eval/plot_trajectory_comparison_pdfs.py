#!/usr/bin/env python3
"""Create black-and-white GT versus calculated trajectory PDFs."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams["font.family"] = "Liberation Serif"


EVAL_DIR = Path("/workspace/eval")
GT_DIR = EVAL_DIR / "gt"
RESULT_DIR = Path("/workspace/results")

MAPPINGS = {
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

METHOD_NAMES = {
    "svo": "svo",
    "orb": "orb_slam3",
    "tsformer": "tsformer_vo",
}

METHOD_COLORS = {
    "svo": "cornflowerblue",
    "orb": "tab:orange",
    "tsformer": "tab:green",
}

METHOD_LEGEND_LABELS = {
    "svo": "Прорачуната путања (SVO)",
    "orb": "Прорачуната путања (ORB-SLAM3)",
    "tsformer": "Прорачуната путања (TSformer-VO)",
}


def read_gt_csv(path: Path) -> np.ndarray:
    positions = []
    with path.open("r", newline="") as file:
        for row in csv.DictReader(file):
            positions.append((float(row["x"]), float(row["y"])))
    return np.asarray(positions, dtype=float)


def read_pose_file(path: Path) -> np.ndarray:
    positions = []
    with path.open("r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 12:
                continue
            values = parts[1:13] if len(parts) == 13 else parts[:12]
            try:
                pose = np.asarray([float(value) for value in values]).reshape(3, 4)
            except ValueError:
                continue
            positions.append((pose[0, 3], pose[1, 3]))
    return np.asarray(positions, dtype=float)


def method_path(method: str, sequence_id: str) -> Path:
    if method == "svo":
        return RESULT_DIR / "svo" / "aligned" / f"{sequence_id}.txt"
    if method == "orb":
        return RESULT_DIR / "orb" / "aligned" / f"{sequence_id}.txt"
    if method == "tsformer":
        return RESULT_DIR / "TSformer-VO" / "Model3" / "aligned" / f"{sequence_id}.txt"
    raise ValueError(f"Unknown method: {method}")


FAMILY_TITLES = {
    "curve_fast": "Криволинијска секвенца - брза",
    "curve_slow": "Криволинијска секвенца - спора",
    "straight_fast": "Праволинијска секвенца - брза",
    "straight_slow": "Праволинијска секвенца - спора",
}


def plot_comparison(ax, family: str, mapping: dict, selected_method=None):
    gt_positions = read_gt_csv(GT_DIR / mapping["gt"])
    if len(gt_positions) == 0:
        raise ValueError(f"Empty reference trajectory for {family}")

    ax.plot(
        gt_positions[:, 0], gt_positions[:, 1],
        color="black", linewidth=2.5, linestyle="--", zorder=1,
        label="Референтна путања",
    )

    all_positions = [gt_positions]
    methods_to_plot = METHOD_NAMES if selected_method is None else {selected_method: METHOD_NAMES[selected_method]}
    for method in methods_to_plot:
        calculated_path = method_path(method, mapping[method])
        calculated_positions = read_pose_file(calculated_path)
        if len(calculated_positions) == 0:
            raise ValueError(f"Empty trajectory for {family} / {method}")
        ax.plot(
            calculated_positions[:, 0], calculated_positions[:, 1],
            color=METHOD_COLORS[method], linewidth=2.5, linestyle="-", zorder=2,
            label=METHOD_LEGEND_LABELS[method],
        )
        all_positions.append(calculated_positions)

    # Include every trajectory so calculated excursions are not clipped.
    all_positions = np.vstack(all_positions)
    x_min, y_min = all_positions.min(axis=0)
    x_max, y_max = all_positions.max(axis=0)
    x_margin = max((x_max - x_min) * 0.05, 0.01)
    y_margin = max((y_max - y_min) * 0.05, 0.01)
    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    ax.set_title(FAMILY_TITLES[family], fontsize=16)
    ax.grid(True, alpha=0.3)
    return ax.lines


def main() -> None:
    ordered_families = ["straight_slow", "straight_fast", "curve_slow", "curve_fast"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    legend_lines = None

    for ax, family in zip(axes.flatten(), ordered_families):
        lines = plot_comparison(ax, family, MAPPINGS[family])
        if legend_lines is None:
            legend_lines = lines

    legend_labels = [
        "Референтна путања",
        METHOD_LEGEND_LABELS["svo"],
        METHOD_LEGEND_LABELS["orb"],
        METHOD_LEGEND_LABELS["tsformer"],
    ]
    fig.legend(
        legend_lines,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.005),
        ncol=2,
        fontsize=16,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))

    output_path = EVAL_DIR / "zajedno-rezultati.pdf"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved to {output_path}")

    for method, method_name in METHOD_NAMES.items():
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        legend_lines = None

        for ax, family in zip(axes.flatten(), ordered_families):
            lines = plot_comparison(ax, family, MAPPINGS[family], selected_method=method)
            if legend_lines is None:
                legend_lines = lines

        fig.legend(
            legend_lines,
            ["Референтна путања", METHOD_LEGEND_LABELS[method]],
            loc="upper center",
            bbox_to_anchor=(0.5, 0.99),
            ncol=2,
            fontsize=16,
        )
        fig.tight_layout(rect=(0, 0, 1, 0.95))

        output_path = EVAL_DIR / f"{method_name.replace('_slam3', '').replace('_vo', '')}-rezultati.pdf"
        fig.savefig(output_path, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()