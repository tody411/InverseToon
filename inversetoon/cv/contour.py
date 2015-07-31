# -*- coding: utf-8 -*-
## @package inversetoon.cv.contour
#
#  Contour functions.
#  @author      tody
#  @date        2015/07/31

import numpy as np
import cv2

from inversetoon.data.contour import Contour


## Convert OpenCV segments data into list of numpy array.
#  @param cv_segments segments data from cv2.findContours
def segmentsFromCV(cv_segments):
    segments = []

    for segment in cv_segments:
        print np.array(segment).shape

        segment = np.array(segment).reshape(-1, 2)
        segments.append(segment)

    return segments


## True if the contour is closed.
#  @param hierarchy hierarchy data from cv2.findContours
def closingFromCV(hierarchy):
    if hierarchy is None:
        return False

    for i, hierarchyData in enumerate(hierarchy[0]):
        if hierarchyData[0] == -1:
            if hierarchyData[1] == -1:
                return True
    return False


## Obtain Contour data with OpenCV.
def findContours(I_8U, t):
    ret, T_8U = cv2.threshold(I_8U, t, 255, 0)
    cv_segments, hierarchy = cv2.findContours(T_8U, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    segments = segmentsFromCV(cv_segments)

    closing = closingFromCV(hierarchy)

    return Contour(segments, closing)


## Draw Contour data with OpenCV.
def drawContours(S_8U, contour, color=(255, 255, 255), linewidth=5):
    cv2.drawContours(S_8U, contour.segments(), -1, color, linewidth)


## Contour mask data.
def contourMask(contour, height, width, linewidth=5):
    S_8U = np.zeros((height, width, 3))
    drawContours(S_8U, contour, (255, 255, 255), linewidth)
    S_8U = S_8U[:, :, 0]
    return S_8U