# -*- coding: utf-8 -*-
## @package inversetoon.core.light_estimation.light_estimation_lumo
#
#  inversetoon.core.light_estimation.light_estimation_lumo utility package.
#  @author      tody
#  @date        2015/10/04

import numpy as np
import matplotlib.pyplot as plt

from inversetoon.core.lumo import lumoNormal
from inversetoon.core.light_estimation.light_estimation_common import testToon
from inversetoon.np.norm import normalizeVector


def foreGroundSamples(A_8U, num_xs=30, num_ys=30, alpha=100):
    h, w = A_8U.shape[:2]
    xs = np.linspace(0, w - 1, num_xs)
    ys = np.linspace(0, h - 1, num_ys)

    xs = np.int32(xs)
    ys = np.int32(ys)

    coords = [(x, y) for y in ys for x in xs if A_8U[y, x] > alpha]
    coords = np.array(coords)
    return coords


def luminanceClusters(Is, num_bins=16):
    I_min = np.min(Is)
    I_max = np.max(Is)

    I_ids = np.int32((Is - I_min) * (num_bins - 1) / (I_max - I_min))
    return I_ids


def estimateLightByCluster(N_lumo, I_32F, p_samples):
    xs, ys = p_samples.T
    Is = I_32F[ys, xs]
    Ns = N_lumo[ys, xs, :]

    I_ids = luminanceClusters(Is)

    I_id_max = np.max(I_ids)

    Ns_bright = Ns[I_ids == I_id_max, :]
    L = np.sum(Ns_bright, axis=0)
    L = normalizeVector(L)
    print L
    return L


def estimateLightDir(input_data):
    N_sil = input_data["N_sil"]
    I_sil = input_data["I_sil"]
    cvs_sil = input_data["cvs_sil"]
    I_32F = input_data["I"]
    A_8U = input_data["A"]

    p_samples = foreGroundSamples(A_8U)
    plt.imshow(A_8U)
    plt.scatter(p_samples[:, 0], p_samples[:, 1])
    plt.show()

    N_lumo = lumoNormal(A_8U)

    L = estimateLightByCluster(N_lumo, I_32F, p_samples)
    output_data = {"L": L}

    return output_data

if __name__ == '__main__':
    testToon("Lumo", estimateLightDir)