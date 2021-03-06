
# -*- coding: utf-8 -*-
## @package inversetoon.core.light_estimation
#
#  inversetoon.core.light_estimation utility package.
#  @author      tody
#  @date        2015/09/07

import numpy as np

from inversetoon.np.norm import normalizeVector
from inversetoon.core.light_estimation.light_estimation_common import testToon


def estimateLightDir(input_data):
    N_sil = input_data["N_sil"]
    I_sil = input_data["I_sil"]

    I_positive = I_sil > 0.001

    N_sil = N_sil[I_positive]
    I_sil = I_sil[I_positive]

    NdLs = I_sil
    L = estimateLightDirProjection(N_sil, NdLs)

    output_data = {"L": L}
#     error = np.linalg.norm(np.dot(N_sil, L) - NdLs)

    return output_data


def estimateLightDirLstSq(Ns, NdLs):
    b = NdLs
    A = Ns
    L = np.linalg.lstsq(A, b)[0]
    return L


def estimateLightDirProjection(Ns, NdLs):
    I_maxID = np.argmax(NdLs)
    L = Ns[I_maxID]
    for i in xrange(100):
        for N, NdL in zip(Ns, NdLs):
            NdL_c = np.dot(L, N)
            L = L - NdL_c * N + NdL * N
            L = normalizeVector(L)
    return L


if __name__ == '__main__':
    testToon("LeastSquare", estimateLightDir)
