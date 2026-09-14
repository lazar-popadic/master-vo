import math
import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def parse_timestamp(value):
    if method == "orb":
        integer = int(value.split(".")[0])
        if integer > 1e12:
            return integer / 1e9
    return float(value)


def convert(gt_file, trajectory_file, method):
    output_file = os.path.splitext(gt_file)[0] + "_kitti.txt"
    ground_truth = pd.read_csv(gt_file).sort_values("timestamp")
    timestamps = []
    frame_ids = []

    with open(trajectory_file) as source:
        for line in source:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            if method == "orb":
                timestamps.append(parse_timestamp(parts[0]))
                frame_ids.append(len(frame_ids))
            else:
                if len(parts) < 9:
                    continue
                frame_ids.append(int(parts[0]))
                timestamps.append(float(parts[1]))

    time = ground_truth["timestamp"].to_numpy()
    x = interp1d(time, ground_truth["x"].to_numpy(), fill_value="extrapolate")
    y = interp1d(time, ground_truth["y"].to_numpy(), fill_value="extrapolate")
    phi = interp1d(
        time,
        np.unwrap(ground_truth["phi"].to_numpy()),
        fill_value="extrapolate",
    )

    with open(output_file, "w") as target:
        for frame_id, timestamp in zip(frame_ids, timestamps):
            yaw = float(phi(timestamp))
            pose = np.array(
                [
                    [math.cos(yaw), -math.sin(yaw), 0, float(x(timestamp))],
                    [math.sin(yaw), math.cos(yaw), 0, float(y(timestamp))],
                    [0, 0, 1, 0],
                ]
            )
            values = " ".join(f"{value:.12f}" for value in pose.reshape(-1))
            target.write(f"{frame_id} {values}\n")


if len(sys.argv) != 4 or sys.argv[1] not in {"orb", "svo"}:
    sys.exit(1)

method = sys.argv[1]
convert(sys.argv[2], sys.argv[3], method)
