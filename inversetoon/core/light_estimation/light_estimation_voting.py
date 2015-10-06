
import numpy as np
import matplotlib.pyplot as plt

from inversetoon.np.norm import normalizeVector, normalizeVectors, normVectors
from inversetoon.core.light_estimation.light_estimation_common import testToon
from inversetoon.core.pixel_sampling import PixelSampling
from inversetoon.core.lumo import lumoNormal


def luminanceClusters(Is, num_bins=16):
    I_min = np.min(Is)
    I_max = np.max(Is)

    I_ids = np.int32((Is - I_min) * (num_bins - 1) / (I_max - I_min))
    return I_ids


def estimatePhi(N_sil, I_sil):
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
    L[2] = 0.0
    L = normalizeVector(L)
    return L


def estimateTheta(L_phi, cvs_sil, N_sil, I_32F, A_8U):
    NdL = np.dot(N_sil, L_phi)
    NdL_max_id = np.argmax(NdL)

    p_max = cvs_sil[NdL_max_id]
    N_max = N_sil[NdL_max_id]

    v = - 2.0 * N_max[:2]
    v[1] = - v[1]

    I_samples = []
    p_samples = []

    p_32F = np.float32(np.array(p_max))

    p = np.int32(p_32F)

    while A_8U[p[1], p[0]] > 100:
        p = np.int32(p_32F)
        I_samples.append(I_32F[p[1], p[0]])
        p_samples.append(np.array(p))
        p_32F += v

    I_ids = luminanceClusters(I_samples)
    I_max_id = np.max(I_ids)
    I_max_coord = np.average(np.where(I_ids == I_max_id))
    t_theta = I_max_coord / float(len(I_samples))
    t_theta = 2.0 * (0.5 - t_theta)
    print "t_theta", t_theta
    L_xy = t_theta * L_phi
    L_z = np.sqrt(1.0 - np.dot(L_xy, L_xy))

    L = np.array([L_xy[0], L_xy[1], L_z])

    p_max = p_samples[int(I_max_coord)]

#     plt.imshow(I_32F)
#     plt.scatter(p_max[0], p_max[1])
#     plt.show()

    return L


def estimateLbyDistance(cvs_sil, N_sil, I_32F):
    I_sampling = PixelSampling(I_32F, num_pixels = 10000)
    I_samples = I_sampling.pixels()
    I_coords = I_sampling.coordinates()

    I_large_ids = I_samples > 0.5 * np.max(I_samples)
#     I_max_id = np.argmax(I_samples)
#     I_max_coord = I_coords[I_max_id]
#
#     print I_max_coord, I_samples[I_max_id], np.max(I_samples)
    L = np.array([0.0, 0.0, 0.0])
    hist = 0.0
    for I_large_id in I_large_ids:
        I_coord = I_coords[I_large_id]
        dist = normVectors(cvs_sil - I_coord)
        dist_max = np.max(dist)
        w = np.exp(- (dist ** 2) / (0.2 * dist_max**2))
        w *= 1.0 / np.sum(w)

        L_i = np.dot(w, N_sil)
        L += L_i
        hist += 1.0

    if hist > 0.0:
        L /= hist
    print L

    Lz = np.sqrt(1.0 - np.dot(L, L))
    L[2] = Lz
    print L.shape
    L = normalizeVector(L)
    return L

#     plt.imshow(I_32F)
#     plt.scatter(I_max_coord[0], I_max_coord[1])
#     plt.show()
#     plt.clf()


def estimateLightDir(input_data):
    N_sil = input_data["N_sil"]
    I_sil = input_data["I_sil"]
    cvs_sil = input_data["cvs_sil"]
    I_32F = input_data["I"]
    A_8U = input_data["A"]

    N_lumo = lumoNormal(A_8U)
    plt.imshow(0.5 * N_lumo + 0.5)
    plt.show()

    L_phi = estimatePhi(N_sil, I_sil)

    output_data = {"L": L_phi}

#     L = estimateLbyDistance(cvs_sil, N_sil, I_32F)
#     output_data = {"L": L}
    L = estimateTheta(L_phi, cvs_sil, N_sil, I_32F, A_8U)
    # output_data = {"L": L }
    return output_data

if __name__ == '__main__':
    testToon("Voting", estimateLightDir)