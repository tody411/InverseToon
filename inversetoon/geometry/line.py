
# -*- coding: utf-8 -*-
## @package inversetoon.geometry.line
#
#  Line class.
#  @author      tody
#  @date        2015/08/12

import numpy as np


## Simple line class.
class Line:
    ## Constructor
    def __init__(self, p, q):
        self._p = p
        self._q = q
        peq = np.array([p[0], p[1], 1])
        qeq = np.array([q[0], q[1], 1])
        self._leq = np.cross(peq, qeq)

        self._pq = q - p
        self._pq *= 1.0 / np.linalg.norm(self._pq)

    ## Return the positions of the line.
    def points(self):
        return [self._p, self._q]

    ## Find an intersected point with the given line.
    def intersect(self, l):
        ipeq = np.cross(self._leq, l._leq)
        if ipeq[2] < 0.000:
            return None

        ipeq *= 1.0 / ipeq[2]
        ip = np.array([ipeq[0], ipeq[1]])

        return ip

    ## Return the distance from the given point to closest point on the line.
    def distanceToPoint(self, p):
        vp = p - self._p

        vd = vp - np.dot(self._pq, vp) * self._pq
        d = np.linalg.norm(vd)
        return np.dot(self._pq, p - self._p)
