# -*- coding: utf-8 -*-
## @package inversetoon.core.normal_cone
#
#  Normal cone class.
#  @author      tody
#  @date        2015/08/11

import numpy as np

from inversetoon.np.norm import normalizeVectors, normalizeVector
from inversetoon.core.transform import coordinateFrame
from inversetoon.util.logger import getLogger
logger = getLogger(__name__)


## Provide normal interpolation based on normal cone.
class NormalConeInterpolation:
    ## Constructor
    #  @param N1 normal vector: from.
    #  @param N2 normal vector: to.
    #  @param L  light vector.
    def __init__(self, N1, N2, L=[0.3, 0.5, 0.7], I=None):
        self._L = L
        self._I = I
        self._Lxyz = coordinateFrame(self._L)
        self._N1 = N1
        self._N2 = N2

        self.computeCenter()
        self.computeConeAngles()

    def computeCenter(self):
        if self._I is None:
            self._I = 0.5 * np.dot(self._L, self._N1 + self._N2)
        self._center = self._I * self._L

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


class NormalCone:
## Constructor
    def __init__(self, L=[0.3, 0.5, 0.7], I=0.7, Ns=[]):
        self._L = normalizeVector(np.array(L))
        self._I = I
        self._Ns = Ns
        self._Lxyz = coordinateFrame(self._L)
        self.computeCone()
        self.computeAxisCenter()
        self.computeConeAngles()
        self.computeConeAngleChanges()

    def setNormals(self, Ns):
        self._Ns = Ns

    def normals(self):
        return self._Ns

    def setConeAngles(self, thetas):
        self._thetas = thetas

    def coneAngles(self):
        return self._thetas

    def coneCoordinates(self):
        return self._N_ts

    def coneAngleChanges(self):
        return self._dthetas

    def computeCone(self):
        h_cone = self._I
        r_cone = np.sqrt(1.0 - h_cone ** 2)

        self._h_cone = h_cone
        self._r_cone = r_cone

    def computeAxisCenter(self):
        self._center = self._I * self._L

    def computeConeAngles(self):
        thetas = []
        N_ts = []
        for N in self._Ns:
            N_t = N - self._center
            N_tx = np.dot(N_t, self._Lxyz[0])
            N_ty = np.dot(N_t, self._Lxyz[1])
            thetas.append(np.arctan2(N_tx, N_ty))
            N_ts.append((N_tx, N_ty))
        self._thetas = thetas
        theta_min = np.min(thetas)
        theta_max = np.max(thetas)
        self._theta_range = [theta_min, theta_max]
        self._N_ts = np.array(N_ts)

    def computeConeAngleChanges(self):
        dthetas = np.zeros(self._N_ts.shape[0])

        dthetas[:-1] = np.cross(self._N_ts[1:, :], self._N_ts[:-1, :])
        dthetas[-1] = dthetas[-2]

        self._dthetas = np.array(dthetas)

    def computeIsophoteNormal(self):
        thetas = np.linspace(self._theta_range[0], self._theta_range[1], num=20)
        Ns = []

        h_cone = self._I
        r_cone = np.sqrt(1.0 - h_cone ** 2)

        self._h_cone = h_cone
        self._r_cone = r_cone

        N_h = self._I * self._L

        for theta in thetas:
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            N_r = r_cone * (cos_t * self._Lxyz[0] + sin_t * self._Lxyz[1])
            N = N_h + N_r
            Ns.append(N)

        self._Ns = np.array(Ns)