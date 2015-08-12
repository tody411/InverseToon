# -*- coding: utf-8 -*-
## @package inversetoon.core.normal_cone
#
#  Normal cone class.
#  @author      tody
#  @date        2015/08/11

import numpy as np

from inversetoon.np.norm import normalizeVectors
from inversetoon.core.transform import coordinateFrame
from inversetoon.util.logger import getLogger
logger = getLogger(__name__)


## Provide normal interpolation based on normal cone.
class NormalConeInterpolation:
    ## Constructor
    #  @param N1 normal vector: from.
    #  @param N2 normal vector: to.
    #  @param L  light vector.
    def __init__(self, N1, N2, L=[0.3, 0.5, 0.7], ):
        self._L = L
        self._Lxyz = coordinateFrame(self._L)
        self._N1 = N1
        self._N2 = N2

        self.computeCenter()
        self.computeConeAngles()

    def computeCenter(self):
        self._center = 0.5 * np.dot(self._L, self._N1 + self._N2) * self._L

    def computeConeCoordinate(self, N):
        dN = N - self._center
        dN_x = np.dot(dN, self._Lxyz[0])
        dN_y = np.dot(dN, self._Lxyz[1])
        return dN_x, dN_y

    def computeConeAngle(self, N):
        dN_x, dN_y = self.computeConeCoordinate(N)
        return np.arctan2(dN_x, dN_y)

    def computeConeAngles(self):
        self._theta1 = self.computeConeAngle(self._N1)
        self._theta2 = self.computeConeAngle(self._N2)

    def interpolate(self, parameters):
        return self.interpolate_simple(parameters)

    def interpolate_simple(self, parameters):
        dN1 = self._N1 - self._center
        dN2 = self._N2 - self._center

        dNs = np.array([(1.0 - t) * dN1 + t * dN2 for t in parameters])

        normals = self._center + dNs
        normals = normalizeVectors(normals)

        return normals
