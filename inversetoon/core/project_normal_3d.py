
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

        bi_normal = np.cross(tangent, normal)
        tangents_3D[i] = np.cross(normal, bi_normal)

    tangents_3D = normalizeVectors(tangents_3D)
    return tangents_3D


def smoothing3DVectors(vectors_3D, parameters):
    vectors_3D = smoothing(vectors_3D, parameters, smooth=1000.0)
    vectors_3D = normalizeVectors(vectors_3D)
    return vectors_3D


def projectNormals(tangents_3D, normals):
    normals_smooth = np.array(normals)
    num_points = len(normals)

    for i in range(num_points):
        tangent = tangents_3D[i]
        normal = normals[i]

        bi_normal = np.cross(normal, tangent)
        normals_smooth[i] = np.cross(tangent, bi_normal)
    normals_smooth = normalizeVectors(normals_smooth)
    return normals_smooth


def projectIteration(tangents_3D, normals_3D, parameters, num_iterations=3):
    for iter in xrange(num_iterations):
        tangents_3D = projectTangent3D(tangents_3D, normals_3D)
        tangents_3D = smoothing3DVectors(tangents_3D, parameters)
        normals_3D = projectNormals(tangents_3D, normals_3D)
        normals_3D = smoothing3DVectors(normals_3D, parameters)
    return normals_3D
