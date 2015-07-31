# -*- coding: utf-8 -*-
## @package inversetoon.core.lighting
#
#  inversetoon.core.lighting utility package.
#  @author      tody
#  @date        2015/07/31

import numpy as np

from inversetoon.np.norm import normalizeVector
from inversetoon.cv.normal import normalSphere


## Compute illumination for the normal image and light direction.
#  Illumination value will be in [0, 1].
def computeIllumination(N_32F, L):
    L = normalizeVector(L)
    h, w, cs = N_32F.shape

    N_flat = N_32F.reshape((-1, 3))

    I_flat = np.dot(N_flat, L)
    I_32F = I_flat.reshape((h, w))
    I_32F = 0.5 * I_32F + 0.5
    return I_32F


## Light sphere image for the light direction.
def lightSphere(L, h=256, w=256):
    L = normalizeVector(L)

    N_32F, A_32F = normalSphere(h, w)
    I_32F = computeIllumination(N_32F, L)
    I_32F = I_32F * A_32F
    return I_32F

