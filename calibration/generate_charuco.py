# Updated from https://gist.github.com/robcowie/65880b58707e9399abad758ba75c3b58

import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

dict = cv2.aruco.DICT_6X6_250  # Dictionary ID
v = 7  # Number of squares vertically
h = 5  # Number of squares horizontally
a = 400  # Square side length (in pixels)
m = 300  # ArUco marker side length (in pixels)
mv = 85  # Margins size, vertical (in pixels)
mh = 50  # Margins size, horizontal (in pixels)

IMG_SIZE = (h * a, v * a)
OUTPUT_NAME = "ChArUco_A4_7x5_400A_300M.png"


def generate_board():
    dictionary = cv2.aruco.getPredefinedDictionary(dict)
    board = cv2.aruco.CharucoBoard(
        (h, v),
        a,
        m,
        dictionary,
    )
    img = cv2.aruco.CharucoBoard.generateImage(board, IMG_SIZE)
    image = cv2.copyMakeBorder(
        img, mv, mv, mh, mh, cv2.BORDER_CONSTANT, value=(255, 255, 255)
    )
    height, width = image.shape
    confirmed_image_size = (height, width)
    print(str(IMG_SIZE) + " resized to " + str(confirmed_image_size))
    cv2.imwrite(OUTPUT_NAME, image)


generate_board()
