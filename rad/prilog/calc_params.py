import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import json

dict = cv2.aruco.DICT_6X6_250
v = 7
h = 5
a_mm = 40
m_mm = 30

pixel_per_mm = 600.0 / 25.4
a = round(a_mm * pixel_per_mm)
m = round(m_mm * pixel_per_mm)

directory = "calibration-photos"


def get_calibration_parameters(img_dir):
    dictionary = cv2.aruco.getPredefinedDictionary(dict)
    board = cv2.aruco.CharucoBoard((h, v), a, m, dictionary)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)

    image_files = [
        os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".jpg")
    ]
    all_charuco_ids = []
    all_charuco_corners = []

    for image_file in image_files:
        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgSize = image.shape
        image_copy = image.copy()
        marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(image)

        if len(marker_ids) > 0:
            print("len(marker_ids)" + str(len(marker_ids)))
            ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(
                marker_corners, marker_ids, image, board
            )

            if charucoIds is not None and len(charucoCorners) > 3:
                all_charuco_corners.append(charucoCorners)
                all_charuco_ids.append(charucoIds)

    result, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, all_charuco_ids, board, imgSize, None, None
    )
    return mtx, dist


OUTPUT_JSON = "calibration.json"

mtx, dist = get_calibration_parameters(directory)
data = {"mtx": mtx.tolist(), "dist": dist.tolist()}

with open(OUTPUT_JSON, "w") as json_file:
    json.dump(data, json_file, indent=4)