import os
import sys
import numpy as np
from scipy.spatial.transform import Rotation


def convert(input_file, method):
    output_file = os.path.splitext(input_file)[0] + "_kitti.txt"
    transform = np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]])

    with open(input_file) as source, open(output_file, "w") as target:
        frame_id = 0
        for line in source:
            if not line.strip() or line.startswith("#"):
                continue

            parts = line.split()
            if method == "orb":
                if len(parts) < 8:
                    continue
                position = np.array([float(value) for value in parts[1:4]])
                quaternion = [float(value) for value in parts[4:8]]
                rotation = Rotation.from_quat(quaternion).as_matrix()
                rotation = transform @ rotation @ transform.T
                position = transform @ position
            else:
                if len(parts) < 9:
                    continue
                frame_id = int(parts[0])
                position = np.array([float(value) for value in parts[2:5]])
                quaternion = [float(value) for value in parts[5:9]]
                rotation = Rotation.from_quat(quaternion).as_matrix()

            pose = np.eye(4)
            pose[:3, :3] = rotation
            pose[:3, 3] = position
            values = " ".join(f"{value:.12f}" for value in pose[:3].reshape(-1))
            target.write(f"{frame_id} {values}\n")
            frame_id += 1


if len(sys.argv) != 3 or sys.argv[1] not in {"orb", "svo"}:
    sys.exit(1)

convert(sys.argv[2], sys.argv[1])
