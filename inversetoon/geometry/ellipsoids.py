
# -*- coding: utf-8 -*-
## @package inversetoon.geometry.ellipsoids
#
#  Implementation of 2D ellipsoids.
#  @author      tody
#  @date        2015/08/13

import math
import numpy as np
from numpy.linalg import eig, inv


## Ellipsoids
class Ellipsoids:
    ## Constructor
    def __init__(self, points = []):
        self._A = None
        self._center = None
        self._phi = None
        self._dU = None
        self._dV = None
        self._axes = None
        self._thetas = None

        if len(points) > 0:
            self.fit(points)

    def fit(self, points):
        self.fitParameters(points)

        self.computeCenter()
        self.computeRotation()
        self.computeAxes()
        self.computeThetas(points)

    def fitParameters(self, points):
        points = np.array(points)
        x = points[:, 0]
        y = points[:, 1]
        D = np.array([x * x, x * y, y * y, x, y, np.ones_like(x)])

        S = np.dot(D, D.T)

        C = np.zeros((6, 6))
        C[0, 2] = C[2, 0] = 2
        C[1, 1] = -1
        eigen_values, eigen_vectors = eig(np.dot(inv(S), C))
        maxID = np.argmax(np.abs(eigen_values))
        self._A = eigen_vectors[:, maxID]

    def computeCenter(self):
        A = self._A
        a, b, c, d, f, g = A[0], A[1] / 2, A[2], A[3] / 2, A[4] / 2, A[5]
        num = b * b - a * c
        x0 = (c * d - b * f) / num
        y0 = (a * f - b * d) / num
        self._center = np.array([x0, y0])

    def computeRotation(self):
        A = self._A
        a, b, c, d, f, g = A[0], A[1] / 2, A[2], A[3] / 2, A[4] / 2, A[5]
        phi = 0.5 * np.arctan(2 * b / (a - c))
        self._phi = phi

        dU = np.array([np.cos(phi), np.sin(phi)])
        dV = np.array([-np.sin(phi), np.cos(phi)])

        self._dU = dU
        self._dV = dV

    def computeAxes(self):
        A = self._A
        a, b, c, d, f, g = A[0], A[1] / 2, A[2], A[3] / 2, A[4] / 2, A[5]
        up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
        down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
        down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))

        res1 = res2 = up
        res1 /= down1
        res2 /= down2

        res1=np.max([0.00001, res1])
        res1=np.sqrt(res1)
        res2=np.max([0.00001, res2])
        res2=np.sqrt(res2)

        self._axes = [res1, res2]

    def computeTheta(self, p):
        a, b = self._axes
        phi = self._phi
        c = self._center

        dU = np.array([np.cos(phi), np.sin(phi)])
        dV = np.array([-np.sin(phi), np.cos(phi)])

        cp = p - c
        u, v = [np.dot(cp, dU), np.dot(cp, dV)]
        u /= a
        v /= b

        theta = np.arctan2(v, u)
        return theta

    def computeThetas(self, points):
        self._thetas = [self.computeTheta(p) for p in points]

    def pointAt(self, t):
        a, b = self._axes
        dU = self._dU
        dV = self._dV
        c = self._center

        p = c + a * np.cos(t) * dU + b * np.sin(t) * dV
        return p

    def pointsAt(self, t):
        a, b = self._axes
        dU = self._dU
        dV = self._dV
        a_dU = a * dU
        b_dV = b * dV
        c = self._center

        U = np.array([np.cos(t), np.cos(t)]).T
        V = np.array([np.sin(t), np.sin(t)]).T

        P = c + U * a_dU + V * b_dV
        return P

    def points(self):
        return self.pointsAt(self._thetas)

    def curvatureAt(self, t):
        a, b = self._axes
        u = np.cos(t)
        v = np.sin(t)
        up = a * b
        down = b * b * u * u + a * a * v * v
        down = math.pow(down, 1.5)
        k = up / down
        return k

    def curvatures(self):
        K = [self.curvatureAt(t) for t in self._thetas]
        return K

    def plotCenter(self, plt, color="g"):
        plt.scatter(self._center[0], self._center[1], color=color)

    def plotAxes(self, plt, color=[0.0, 0.2, 0.2]):
        a, b = self._axes
        dU = self._dU
        dV = self._dV
        a_dU = a * dU
        b_dV = b * dV

        c = self._center

        a_axis = np.array([c - a_dU, c + a_dU])
        b_axis = np.array([c - b_dV, c + b_dV])

        plt.plot(a_axis[:,0], a_axis[:,1], "-", color=color)
        plt.plot(b_axis[:,0], b_axis[:,1], "-", color=color)

    def plotEllipsoids(self, plt, color="r"):
        P = self.points()
        plt.plot(P[:,0], P[:,1], "-", color=color)

    def plotCurvatures(self, plt):
        K = self.curvatures()
        x = np.arange(len(K))
        plt.plot(x, K, "-")


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inversetoon.plot.window import showMaximize

    a, b = 4.0, 3.0
    c = 0.2 * np.random.rand(2)
    t_min, t_max = [0.2 * np.pi, 1.2 * np.pi]
    t = np.linspace(t_min, t_max, 100)
    phi = 0.3 * np.pi
    dU = np.array([np.cos(phi), np.sin(phi)])
    dV = np.array([-np.sin(phi), np.cos(phi)])

    U = np.array([np.cos(t), np.cos(t)]).T
    V = np.array([np.sin(t), np.sin(t)]).T

    points = c + a * U * dU + b * V * dV
    points[:, 0] += 0.1 * np.random.rand(len(t))
    points[:, 1] += 0.1 * np.random.rand(len(t))

    ax = plt.subplot(121)
    ax.set_aspect('1.0')

    ax.scatter(points[:, 0], points[:, 1])

    el = Ellipsoids(points)
    el.plotCenter(ax)
    el.plotAxes(ax)
    el.plotEllipsoids(ax)

    ax2 = plt.subplot(122)
    el.plotCurvatures(ax2)
    showMaximize()