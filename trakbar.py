import cv2
import numpy as np


def nothing(img):
    pass


cv2.namedWindow("trackbar")
cv2.createTrackbar("h", "trackbar", 0, 200, nothing)

while True:
    i = 1
