import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

dict = cv2.aruco.DICT_6X6_250
v = 7  # Number of squares vertically
h = 5  # Number of squares horizontally
a_mm = 40  # Square side length (in mm)
m_mm = 30  # ArUco marker side length (in mm)
mv_mm = 8.5  # Margins size, vertical (in mm)
mh_mm = 5.0  # Margins size, horizontal (in mm)
print_margin_mm = 5.0  # printer limitation (in mm)

pixel_per_mm = 600.0 / 25.4
a = round(a_mm * pixel_per_mm)
m = round(m_mm * pixel_per_mm)
mv = round((mv_mm - print_margin_mm) * pixel_per_mm)
mh = round((mh_mm - print_margin_mm) * pixel_per_mm)

IMG_SIZE = (h * a, v * a)
OUTPUT_NAME = "ChArUco_A4_7x5_40A_30M.png"


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
    # additional margin for printing, empirical
    mh_print = 50
    mv_print = round(mh_print * 297.0 / 210.0)
    print_image = cv2.copyMakeBorder(
        image, mv, mv, mh, mh, cv2.BORDER_CONSTANT, value=(255, 255, 255)
    )
    cv2.imwrite(OUTPUT_NAME, print_image)


generate_board()
