
import numpy as np
import matplotlib.pyplot as plt

from inversetoon.np.norm import normalizeVector, normalizeVectors
from inversetoon.core.light_estimation.light_estimation_common import testToon
from inversetoon.core.pixel_sampling import PixelSampling


def luminanceClusters(Is, num_bins=16):
    I_min = np.min(Is)
    I_max = np.max(Is)

    I_ids = np.int32((Is - I_min) * (num_bins - 1) / (I_max - I_min))
    return I_ids


def estimatePhi(N_sil, I_sil):
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

    I_id_max = np.max(np.where(hist_positive))
    L = N_centers[I_id_max]
    return L


def estimateLbyDistance(cvs_sil, N_sil, I_32F):
    I_sampling = PixelSampling(I_32F, num_pixels = 10000)
    I_samples = I_sampling.pixels()
    I_coords = I_sampling.coordinates()

    I_max_id = np.argmax(I_samples)
    I_max_coord = I_coords[I_max_id]

    print I_max_coord, I_samples[I_max_id], np.max(I_samples)

    plt.imshow(I_32F)
    plt.scatter(I_max_coord[0], I_max_coord[1])
    plt.show()
    plt.clf()

def estimateLightDir(input_data):
    N_sil = input_data["N_sil"]
    I_sil = input_data["I_sil"]
    cvs_sil = input_data["cvs_sil"]
    I_32F = input_data["I"]

    L_phi = estimatePhi(N_sil, I_sil)

    output_data = {"L": L_phi}

    estimateLbyDistance(cvs_sil, N_sil, I_32F)
    return output_data

if __name__ == '__main__':
    testToon("Voting", estimateLightDir)