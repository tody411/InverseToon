
# -*- coding: utf-8 -*-
## @package inversetoon.data.isophote_segment
#
#  Isophote segment data definition.
#  @author      tody
#  @date        2015/07/30

import numpy as np
from inversetoon.np.norm import normVectors, normalizeVectors

from inversetoon.core.transform import coordinateFrame

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)


## Compute arc-length parameters from points.
def computeArcLengthParameters(points):
    diff_points = points[1:, :] - points[:-1, :]
    dist_points = normVectors(diff_points)

    dist_sum = np.sum(dist_points)

    parameters = np.zeros(len(points))

    arc_length = 0
    for pi in range(len(dist_points)):
        arc_length += dist_points[pi]
        parameters[pi + 1] = arc_length / dist_sum

    logger.debug("Total arc length: %s" % dist_sum)

    return parameters


## Comute curvatures from points.
def computeCurvatures(points):
    t1 = np.array(points, dtype=np.float)
    t2 = np.array(points, dtype=np.float)

    t1[1:] = points[1:] - points[:-1]
    t2[:-1] = points[1:] - points[:-1]

    t1_norm = np.linalg.norm(t1, axis=1)
    t2_norm = np.linalg.norm(t2, axis=1)
    t1t2_norm = np.linalg.norm(t1 + t2, axis=1)

    k_bottom = t1_norm + t2_norm + t1t2_norm

    k_top = 2.0 * np.cross(t1, t2)

    k = k_top / k_bottom
    k[0] = k[1]
    k[-1] = k[-2]
    return k


## Compute tangent vectors from points.
def computeTangents(points):
    t1 = np.array(points, dtype=np.float)
    t2 = np.array(points, dtype=np.float)

    t1[1:] = points[1:] - points[:-1]
    t2[:-1] = points[1:] - points[:-1]
    t1[0] = t1[1]
    t2[-1] = t2[-2]

    t = t1

    t = normalizeVectors(t)
    t[:, 1] = - t[:, 1]

    return t


## Isophote segment data class.
#
#  Attributes:
#  * points: n x 2 numpy array.
#  * normals: n x 2 numpy array.
#  * arc_lengh_parameters: n numpy vector.
#  * curvatures: n numpy vector.
#  * tangents: n x 2 numpy array.
#  * L: light direction for the isophote.
#  * Lxyz: light coordinate frame.
#  * cvIDs: Control vertex IDs.
class IsophoteSegment:
    ## Constructor
    #  @param  points  2 x n numpy array.
    def __init__(self, points=[], cvIDs=[]):
        self._points = points
        self._cvIDs = cvIDs
        self._arc_lengh_parameters = None
        self._curvatures = None
        self._tangents = None
        self._normals = None
        self._L = np.array([0.0, 0.0, 1.0])
        self._Lxyz = coordinateFrame(self._L)
        self._cone_angles = None

    def setLightDir(self, L):
        self._L = L

    def lightDir(self):
        return self._L

    def setPoints(self, points):
        self._points = points

    def points(self):
        return self._points

    def setCVIDs(self, cvIDs):
        self._cvIDs = cvIDs

    def CVIDs(self):
        return self._cvIDs

    def arcLengthParameters(self):
        if self._arc_lengh_parameters is None:
            self._arc_lengh_parameters = computeArcLengthParameters(self._points)
        return self._arc_lengh_parameters

    def curvatures(self):
        if self._curvatures is None:
            self._curvatures = computeCurvatures(self._points)
        return self._curvatures

    def tangents(self):
        if self._tangents is None:
            self._tangents = computeTangents(self._points)
        return self._tangents

    def setNormals(self, normals):
        self._normals = normals

    def normals(self):
        return self._normals

    def __str__(self):
        info = "CurveSegment:\n"
        info += "  Num Points: %s\n" % len(self._points)
        info += "  Num Normals: %s\n" % len(self._normals)
        return info
