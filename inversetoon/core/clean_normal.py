# -*- coding: utf-8 -*-
## @package inversetoon.core.clean_normal
#
#  inversetoon.core.clean_normal utility package.
#  @author      tody
#  @date        2015/10/03

import numpy as np
import cv2
import matplotlib.pyplot as plt
from inversetoon.datasets.normal import dataNames, loadData, saveData
from inversetoon.cv.normal import normalizeImage
from inversetoon.np.norm import normVectors
from inversetoon.cv.image import to32F, to8U


def cleanNormal(N_32F, A_8U):
    # N_32F = cv2.bilateralFilter(N_32F, 0, 0.1, 5)
    h, w = N_32F.shape[:2]

    plt.subplot(1, 2, 1)
    plt.gray()
    plt.imshow(normVectors(N_32F.reshape(-1, 3)).reshape(h, w))

    plt.subplot(1, 2, 2)
    plt.gray()
    A_32F = to32F(A_8U)
    A_32F = cv2.GaussianBlur(A_32F, (0, 0), 3.0)
    A_32F = np.clip(10.0 * (A_32F - 0.5) + 0.5, 0.0, 1.0)
    A_32F = cv2.GaussianBlur(A_32F, (0, 0), 3.0)
    N_fix = A_32F > 0.9
    N_bg = A_32F < 0.25
    A_32F = np.clip(10.0 * (A_32F - 0.5) + 0.5, 0.0, 1.0)
    A_8U = to8U(A_32F)
#     plt.imshow(A_8U)
#     plt.show()

    N_32F_blur = cv2.GaussianBlur(N_32F, (0, 0), 3.0)
    for i in xrange(10):
        N_32F_blur = cv2.GaussianBlur(N_32F_blur, (0, 0), 3.0)
        N_32F_blur[N_fix, :] = N_32F[N_fix, :]

    N_32F = N_32F_blur
    # N_32F[N_bg, 2] = 0.0
    N_32F_normalized = normalizeImage(N_32F)

    #A_8U = np.uint8(np.clip(1000.0 * N_32F_normalized[:, :, 2], 0.0, 255.0))
    # A_8U = cv2.bilateralFilter(A_8U, 0, 70, 5)

    return N_32F_normalized, A_8U


def cleanNormalBatch():
    target = "original"
    for data_name in dataNames(target="original"):
        N_32F, A_8U = loadData(data_name, target)

        N_32F, A_8U = cleanNormal(N_32F, A_8U)
        saveData(data_name, N_32F, A_8U, target="normal")

if __name__ == '__main__':
    cleanNormalBatch()
