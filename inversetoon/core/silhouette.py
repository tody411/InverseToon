# -*- coding: utf-8 -*-
## @package inversetoon.core.silhouette
#
#  Silhoutte functions.
#  @author      tody
#  @date        2015/07/31

import numpy as np
import cv2

from inversetoon.cv.contour import findContours, contourMask
from inversetoon.data.curve import NormalCurve
from inversetoon.cv.image import to32F


## Silhouette normal from the alpha mask.
def silhouetteNormal(A_8U, sigma=7.0):
    height, width = A_8U.shape[0], A_8U.shape[1]

    A_8U_blur = cv2.GaussianBlur(A_8U, (0, 0), sigma)
    A_8U_blur = to32F(A_8U_blur)

    gx = cv2.Sobel(A_8U_blur, cv2.CV_64F, 1, 0, ksize=5)
    gy = cv2.Sobel(A_8U_blur, cv2.CV_64F, 0, 1, ksize=5)

    N_32F = np.zeros((height, width, 3), dtype=np.float32)

    N_32F[:, :, 0] = -gx
    N_32F[:, :, 1] = gy
    N_32F[:, :, 2] = A_8U_blur

    gxy_norm = np.zeros((height, width))

    gxy_norm[:, :] = np.sqrt(gx[:, :] * gx[:, :] + gy[:, :] * gy[:, :])

    Nxy_norm = np.zeros((height, width))
    Nxy_norm[:, :] = np.sqrt(1.0 - A_8U_blur[:, :])

    wgxy = np.zeros((height, width))
    wgxy[:, :] = Nxy_norm[:, :] / (0.001 + gxy_norm[:, :])

    N_32F[:, :, 0] = wgxy[:, :] * N_32F[:, :, 0]
    N_32F[:, :, 1] = wgxy[:, :] * N_32F[:, :, 1]

    return N_32F


def silhoutteCurve(A_8U):
    h, w = A_8U.shape
    contour = findContours(A_8U, 200.0)
    contour.resample(span=5)

    silhoutteCurve = NormalCurve()
    silhoutteCurve.setContour(contour)

    silhoutte_contour = findContours(A_8U, 127.0)

    S_8U = contourMask(silhoutte_contour, h, w)
    S_8U[A_8U < 127] = 255
    return silhoutteCurve, S_8U
