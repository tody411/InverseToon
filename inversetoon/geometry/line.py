
# -*- coding: utf-8 -*-
## @package inversetoon.geometry.line
#
#  Implementation of a 2D line.
#  @author      tody
#  @date        2015/08/12

import numpy as np
from inversetoon.np.norm import normalizeVector
from inversetoon.geometry.bounding_box import BoundingBox


## Implementation of a 2D line.
class Line:
    ## Constructor
    #
    #  @param p start point
    #  @param q end point
    #
    #  Line representation: (a, b, c) = (x1, y1, 1) $\times$ (x2, y2, 1)
    #  - points on line: (a, b, c) $\cdot$ (x, y , 1) = 0
    #  - line intersection: (x, y, w) = (a1, b1, c1) $\times$ (a2, b2, c2)
    def __init__(self, p, q):
        self._p = np.array(p)
        self._q = np.array(q)
        peq = np.array([p[0], p[1], 1])
        qeq = np.array([q[0], q[1], 1])
        self._n = np.cross(peq, qeq)
        self._n = normalizeVector(self._n)

        self._e = self._q - self._p
        self._e = normalizeVector(self._e)
        self._bb = BoundingBox([p, q])

    ## Return the positions of the line.
    def points(self):
        return np.array([self._p, self._q])

    ## Return the position of the parameter [0, 1].
    def pointAt(self, t):
        return self._p + t * self.length() * self._e

    ## Return the length of the line.
    def length(self):
        return np.linalg.norm(self._q - self._p)

    ## Find an intersected point with the given line.
    def intersect(self, l):
        ipeq = np.cross(self._n, l._n)
        if np.abs(ipeq[2]) < 0.000:
            return None

        ipeq *= 1.0 / ipeq[2]
        ip = np.array([ipeq[0], ipeq[1]])

        if self._bb.contains(ip) and l._bb.contains(ip):
            return ip

        return None

    ## Returns the closest point on this line to the given point.
    def closestPoint(self, p):
        return self._closestPointVec(p)

    ## Returns the closest point on this line to the given point.
    def _closestPointEq(self, p):
        a, b, c = self._n
        x0, y0 = p

        x = (b * (b * x0 - a * y0) - a * c) / (a * a + b * b)
        y = (a * (-b * x0 + a * y0) - b * c) / (a * a + b * b)
        return np.array([x, y])

    ## Returns the closest point on this line to the given point.
    def _closestPointVec(self, p):
        v = p - self._p
        return np.dot(v, self._e) * self._e + self._p

    ## Return the parameter of the closest point.
    def closestParam(self, p):
        v = p - self._p
        t = np.dot(v, self._e)
        return t / self.length()

    ## Return the distance from the given point to closest point on the line.
    def distanceToPoint(self, p):
        a, b, c = self._n
        x0, y0 = p

        return np.abs((a * x0 + b * y0 + c) / np.sqrt(a ** 2 + b ** 2))

    ## Plot line with matplot.
    def plotLine(self, plt):
        ps = self.points()
        plt.plot(ps[:, 0], ps[:, 1], "-")

    def plotVector(self, plt):
        hl = 0.02
        v = self._q - self._p
        v *= 1.0 - 2.0 * hl
        plt.arrow(self._p[0], self._p[1], v[0], v[1], head_width=0.5 * hl, head_length=hl)

    ## Plot closest point.
    def plotClosetPoint(self, plt, p):
        p = np.array(p)
        cp = self.closestPoint(p)
        plt.plot(cp[0], cp[1], "o")
        plt.annotate('closest point: %s' % cp, xy=cp)

        Line(p, cp).plotLine(plt)
        Line(self._p, p).plotVector(plt)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inversetoon.plot.window import showMaximize
    l1 = Line((0.0, 0.2), (1.0, 1.0))
    l2 = Line((0.0, 1.0), (1.0, 0.0))
    p = np.array((0.2, 0.6))

    ax = plt.subplot(111)
    ax.set_aspect('1.0')

    l1.plotLine(ax)
    l2.plotLine(ax)

    ip = l1.intersect(l2)
    t = l1.closestParam(ip)

    plt.title("Intersect at t, p: %s, %s" % (t, ip))

    ax.plot(ip[0], ip[1], "o")
    ax.plot(p[0], p[1], "o")

    l1.plotClosetPoint(plt, p)

    ax.set_aspect('1.0')
    showMaximize()
