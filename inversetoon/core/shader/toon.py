import numpy as np
from inversetoon.np.norm import normalizeVector

import half_lambert


## Compute illumination for the normal image and light direction.
#  Illumination value will be in [0, 1].
def diffuse(N_32F, L, borders=[0.5], colors=[np.array([0.2, 0.2, 0.5]), np.array([0.5, 0.5, 0.8])]):
    print L
    L = normalizeVector(L)
    print L
    I_32F = half_lambert.diffuse(N_32F, L)

    h, w, cs = N_32F.shape

    C_32F = np.zeros((h, w, cs), dtype=np.float32)
    I_32F_flat = I_32F.reshape(h * w)
    C_32F_flat = C_32F.reshape(-1, 3)

    C_32F_flat[:, :] = colors[0]

    for border, color in zip(borders, colors[1:]):
        C_32F_flat[I_32F_flat > border, :] = color

    return C_32F