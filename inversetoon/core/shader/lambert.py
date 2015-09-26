import numpy as np
from inversetoon.np.norm import normalizeVector


## Compute illumination for the normal image and light direction.
#  Illumination value will be in [0, 1].
def diffuse(N_32F, L):
    L = normalizeVector(L)
    h, w, cs = N_32F.shape

    N_flat = N_32F.reshape((-1, 3))

    I_flat = np.dot(N_flat, L)
    I_32F = I_flat.reshape((h, w))
    I_32F = np.clip(I_32F, 0.0, 1.0)
    return I_32F
