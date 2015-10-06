# -*- coding: utf-8 -*-
## @package inversetoon.core.lumo
#
#  inversetoon.core.lumo utility package.
#  @author      tody
#  @date        2015/10/02

import numpy as np
import pyamg
from pyamg.gallery import laplacian

from inversetoon.core.silhouette import silhouetteNormal
from inversetoon.np.norm import normalizeVectors


## Normal constraints from the alpha mask and the initial normal.
def normalConstraints(A_8U, N0_32F, alpha_th=20, w_sil=1e+10):
    h, w = A_8U.shape

    L = laplacian.poisson((h, w))
    L_lil = L.tolil()

    A_flat = A_8U.flatten()
    sil_ids = np.where(A_flat < alpha_th)

    for sil_id in sil_ids:
        L_lil[sil_id, sil_id] = w_sil

    A = L_lil.tocsr()

    N0_flat = N0_32F.reshape(h * w, 3)
    N0_flat[A_flat > alpha_th, :] = 0.0
    b_all = w_sil * N0_flat
    b = np.zeros(b_all.shape)
    b[A_flat < alpha_th, :] = b_all[A_flat < alpha_th, :]

    return A, b


def solveMG(A, b):
    ml = pyamg.smoothed_aggregation_solver(A)

    x = np.zeros(b.shape)
    for bi in range(3):
        x[:, bi] = ml.solve(b[:, bi], tol=1e-10)
    return x


def lumoNormal(A_8U):
    h, w = A_8U.shape
    N0_32F = silhouetteNormal(A_8U)
    A, b = normalConstraints(A_8U, N0_32F)

    N_flat = solveMG(A, b)
    N_flat = normalizeVectors(N_flat)
    N_32F = N_flat.reshape(h, w, 3)

    return N_32F
