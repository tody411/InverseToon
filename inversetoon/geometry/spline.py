# -*- coding: utf-8 -*-
## @package inversetoon.geometry.spline
#
#  Implementation of 2D spline.
#  @author      tody
#  @date        2015/08/13

import numpy as np
from scipy.interpolate import UnivariateSpline
from inversetoon.np.norm import normVectors


## Implementation of 2D spline.
class Spline:
    ## Constructor
    def __init__(self, cvs=[], smooth=None):
        self._cvs = None
        self._params = None
        self._smooth = None
        self._spl = None

        if len(cvs) > 0:
            self.create(cvs, smooth=smooth)

    def create(self, cvs, smooth=None):
        self._smooth = smooth
        cvs = np.array(cvs)
        self._cvs = cvs
        self.computeParameters()
        self.createSpline()

    def cvs(self):
        return self._cvs

    def computeParameters(self):
        cvs = self._cvs

        diff_cvs = cvs[1:, :] - cvs[:-1, :]
        dist_cvs = normVectors(diff_cvs)

        al_total = np.sum(dist_cvs)

        params = np.zeros(len(cvs))

        al = 0
        for pi in range(len(cvs) - 1):
            al += dist_cvs[pi]
            params[pi + 1] = al

        if al_total > 0.00001:
            params *= (1.0 / al_total)

        self._params = params

    def createSpline(self):
        x, y = self._cvs.T
        t = self._params
        fx = UnivariateSpline(t, x, s=self._smooth)
        fy = UnivariateSpline(t, y, s=self._smooth)

        self._spl = [fx, fy]

    def pointAt(self, t):
        fx, fy = self._spl
        p = np.array([fx(t), fy(t)])
        return p

    def pointsAt(self, t):
        fx, fy = self._spl
        P = np.array([fx(t), fy(t)])
        return P.T

    def points(self):
        return self.pointsAt(self._params)

    def curvatureAt(self, t):
        fx, fy = self._spl
        x_d1 = fx.derivative(1)(t)
        x_d2 = fx.derivative(2)(t)
        y_d1 = fy.derivative(1)(t)
        y_d2 = fy.derivative(2)(t)

        up = x_d1 * y_d2 - y_d1 * x_d2
        down = np.power(x_d1 ** 2 + y_d1 ** 2, 1.5)
        k = up / down
        return k

    def curvaturesAt(self, ts):
        K = [self.curvatureAt(t) for t in ts]
        return K

    def plotCVs(self, plt):
        cvs = self._cvs
        plt.scatter(cvs[:,0], cvs[:,1])

    def plotSpline(self, plt):
        t = np.linspace(0.0, 1.0, 100)
        P = self.pointsAt(t)
        print P
        plt.plot(P[:, 0], P[:, 1], "-")

    def plotCurvatures(self, plt):
        t = np.linspace(0.0, 1.0, 100)
        K = self.curvaturesAt(t)
        x = np.arange(len(K))
        plt.plot(x, K, "-")

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inversetoon.plot.window import showMaximize

    x = np.linspace(0.0, 1.0, 4)
    y = np.random.rand(len(x))
    cvs = np.array([x, y]).T
    spl = Spline(cvs, 0.0001)
    cvs = spl.pointsAt(np.linspace(0.0, 1.0, 30))

    cvs += 0.05 * np.random.rand(len(cvs), 2)
    spl = Spline(cvs)

    plt.subplot(121)
    spl.plotCVs(plt)
    spl.plotSpline(plt)

    plt.subplot(122)
    spl.plotCurvatures(plt)
    showMaximize()
