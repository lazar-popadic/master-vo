import matplotlib.pyplot as plt
import numpy as np
import queue
import pickle
import os
from datasets.kitti import KITTI
from datasets.utils import euler_to_rotation


def save_trajectory(poses, sequence, save_dir):
    """
    Save predicted poses in .txt file
    Args:
        poses {ndarray}: list with all 4x4 pose matrix
        sequence {str}: sequence of KITTI dataset
        save_dir {str}: path to save pose
    """
    # create directory
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    output_filename = os.path.join(save_dir, "{}.txt".format(sequence))
    with open(output_filename, "w") as f:
        for pose in poses:
            pose = pose.flatten()[:12]
            line = " ".join([str(x) for x in pose]) + "\n"
            f.write(line)


def load_optimized_kitti(filepath):
    """Load optimized poses from evo_traj output (.kitti file)"""
    pred_poses = []
    with open(filepath, 'r') as f:
        for line in f:
            vals = [float(x) for x in line.strip().split()]
            if len(vals) == 12:
                T = np.eye(4)
                T[0:3, :] = np.array(vals).reshape(3, 4)
                pred_poses.append(T)
    return pred_poses


if __name__ == "__main__":
  
    ckpt_path = "models/Model3"
    ckpt_name = "checkpoint_model3_exp20"
    sequences = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]

    # read hyperparameters and configuration
    with open(os.path.join(ckpt_path, "args.pkl"), 'rb') as f:
        args = pickle.load(f)
    f.close()

    ckpt_path = os.path.join(ckpt_path, ckpt_name)
    args["checkpoint_path"] = ckpt_path

    # plot trajectory and ground truth
    for sequence in sequences:
        # LOAD OPTIMIZED POSES FROM evo_traj OUTPUT
        optimized_file = os.path.join(args["checkpoint_path"], "opti_poses", "{}.kitti".format(sequence))
        pred_poses = load_optimized_kitti(optimized_file)
        pred_trajectory = [pose[:3, 3] for pose in pred_poses]

        # get ground truth trajectories
        test_data = KITTI(sequences=[sequence], window_size=args["window_size"], camera_id="0")
        gt_poses = test_data.windowed_data.loc[test_data.windowed_data["sequence"]==sequence, [3, 7, 11]]

        plt.figure()
        pred_trajectory = np.asarray(pred_trajectory)
        plt.plot([x[0] for x in pred_trajectory], [z[2] for z in pred_trajectory], "b")  # plot estimated trajectory
        plt.plot([x[0] for x in gt_poses.values], [z[2] for z in gt_poses.values], "r")  # plot ground truth trajectory
        plt.grid()
        plt.title("VO - Seq {}".format(sequence))
        plt.xlabel("Translation in x direction [m]")
        plt.ylabel("Translation in z direction [m]")
        plt.legend(["estimated", "ground truth"]);

        # create checkpoints folder
        if not os.path.exists(os.path.join(args["checkpoint_path"], "opti_plots")):
            os.makedirs(os.path.join(args["checkpoint_path"], "opti_plots"))
        plt.savefig(os.path.join(args["checkpoint_path"], "opti_plots", "opti_traj_{}.png".format(sequence)))