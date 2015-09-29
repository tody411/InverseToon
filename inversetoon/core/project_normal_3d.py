
# -*- coding: utf-8 -*-
## @package inversetoon.core.project_normal_3d
#
#  inversetoon.core.project_normal_3d utility package.
#  @author      tody
#  @date        2015/08/12

import numpy as np
from inversetoon.np.norm import normalizeVectors
from inversetoon.core.smoothing import smoothing


def projectTangent3D(tangents_2D, normals):
    num_points = len(tangents_2D)
    tangents_3D = np.zeros((num_points, 3))
    tangents_3D[:, 0] = tangents_2D[:, 0]
    tangents_3D[:, 1] = tangents_2D[:, 1]

    for i in range(num_points):
        tangent = tangents_3D[i]
        normal = normals[i]

        tangents_3D[i, 2] = - (normal[0] * tangent[0] + normal[1] * tangent[1]) / normal[2]

    # tangents_3D = normalizeVectors(tangents_3D)
    return tangents_3D


def smoothing3DVectors(vectors_3D, parameters):
    vectors_3D = smoothing(vectors_3D, parameters, smooth=0.01)
    vectors_3D = normalizeVectors(vectors_3D)
    return vectors_3D


def smoothingTangentZ(tangents_3D, parameters):
    tangents_3D[:, 2] = smoothing(tangents_3D[:, 2], parameters, smooth=1.0)
    return tangents_3D


def projectNormals(L, I, tangents_3D, normals):
    normals_smooth = np.array(normals)
    num_points = len(normals)

    for i in range(num_points):
        T = tangents_3D[i]
        N = normals[i]

        NdL = np.dot(N, L)

        dN_L = (I - NdL) * L

        NdT = np.dot(N, T)
        dN_T = - NdT * T

        normals_smooth[i] = N + dN_L + dN_T
    normals_smooth = normalizeVectors(normals_smooth)
    return normals_smooth


def preserveEndPoints(N_st, N_ed, normals_3D, sigma=0.05):
    params = np.linspace(0.0, 1.0, len(normals_3D))

    w_st = np.exp( - params * params / (sigma * sigma))
    params_inv = 1.0 - params
    w_ed = np.exp( - params_inv * params_inv / (sigma * sigma))

    for i in range(3):
        normals_3D[:, i] = (1.0 - w_st) * normals_3D[:, i] + w_st * N_st[i]
        normals_3D[:, i] = (1.0 - w_ed) * normals_3D[:, i] + w_ed * N_ed[i]


def projectIteration(L, I, tangents_3D, normals_3D, parameters, num_iterations=3):

    N_st = normals_3D[0]
    N_ed = normals_3D[-1]

    I = 0.5 * (np.dot(N_st, L) + np.dot(N_ed, L))

    for iter in xrange(num_iterations):
        tangents_3D = projectTangent3D(tangents_3D, normals_3D)
        tangents_3D = smoothingTangentZ(tangents_3D, parameters)
        tangents_3D = smoothing3DVectors(tangents_3D, parameters)
        normals_3D = projectNormals(L, I, tangents_3D, normals_3D)
        preserveEndPoints(N_st, N_ed, normals_3D)
        normals_3D = smoothing3DVectors(normals_3D, parameters)
    return normals_3D
