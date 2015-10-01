
import numpy as np

from inversetoon.np.norm import normalizeVector, normalizeVectors
from inversetoon.core.light_estimation.light_estimation_common import testToon


def luminanceClusters(Is, num_bins=16):
    I_min = np.min(Is)
    I_max = np.max(Is)

    I_ids = np.int32((Is - I_min) * (num_bins - 1) / (I_max - I_min))
    return I_ids


def estimateLightDir(N_sil, I_sil):
    I_maxID = np.argmax(I_sil)
    L = N_sil[I_maxID]

    num_bins = 16
    I_ids = luminanceClusters(I_sil, num_bins)

    N_centers = np.zeros((num_bins, 3))
    hist = np.zeros((num_bins))

    for ni, I_id in enumerate(I_ids):
        N_centers[I_id] += N_sil[ni]
        hist[I_id] += 1.0

    hist_positive = hist > 0.0

    N_centers[hist_positive] = normalizeVectors(N_centers[hist_positive])

if __name__ == '__main__':
    testToon("Voting", estimateLightDir)