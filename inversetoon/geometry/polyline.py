# -*- coding: utf-8 -*-
## @package inversetoon.geometry.polyline
#
#  Polyline class.
#  @author      tody
#  @date        2015/08/12

import numpy as np


## Polyline class.
class Polyline:
    ## Constructor
    def __init__(self, points):
        self._points = points
        self._q = q
        peq = np.array([p[0], p[1], 1])
        qeq = np.array([q[0], q[1], 1])
        self._leq = np.cross(peq, qeq)

        self._pq = q - p
        self._pq *= 1.0 / np.linalg.norm(self._pq)

    def intersect(self, l):
        ipeq = np.cross(self._leq, l._leq)
        if ipeq[2] < 0.000:
            return None

        ipeq *= 1.0 / ipeq[2]
        ip = np.array([ipeq[0], ipeq[1]])

        return ip

    def distance(self, p):
        return np.dot(self._pq, p - self._p)

