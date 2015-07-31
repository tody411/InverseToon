# -*- coding: utf-8 -*-
## @package inversetoon.cv.normal
#
#  Normal image functions.
#  @author      tody
#  @date        2015/07/30



import numpy as np
import cv2

from inversetoon.cv.image import rgb, to32F, to8U, setAlpha, alpha
from inversetoon.np.norm import normalizeVectors
from inversetoon.util.timer import timing_func


## RGBA to normal.
def colorToNormal(C_8U, fill_background=True):
    rgb_8U = rgb(C_8U)
    A_8U = alpha(C_8U)

    C_32F = to32F(rgb_8U)

    N_32F = 2.0 * C_32F - 1.0

    if fill_background:
        N_32F[A_8U < 10, :] = np.array([0.0, 0.0, 0.0])

    N_32F_normalized = normalizeImage(N_32F)

    return N_32F_normalized


## Normal to RGB.
def normalToColor(N_32F, A_8U=None):
    C_32F = 0.5 * N_32F + 0.5
    C_8U = to8U(C_32F)

    if A_8U is not None:
        C_8U = setAlpha(C_8U, A_8U)

    return C_8U


## Normalize the normal image.
def normalizeImage(N_32F):
    N_flat = N_32F.reshape((-1, 3))
    N_flat_normalized = normalizeVectors(N_flat)

    N_32F_normalized = N_flat_normalized.reshape(N_32F.shape)
    return N_32F_normalized
