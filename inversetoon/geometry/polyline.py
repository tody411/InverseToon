# -*- coding: utf-8 -*-
## @package inversetoon.geometry.polyline
#
#  Implementation of 2D polyline.
#  @author      tody
#  @date        2015/08/12

import numpy as np
from inversetoon.geometry.bounding_box import BoundingBox
from inversetoon.geometry.line import Line
from inversetoon.util.timer import timing_func


## Simple bounding box hierarchy for the given polints.
#
#  Usage:
#  ```
#  bvh1 = BVH(points1)
#  bvh2 = BVH(points2)
#  ibvhs = bvh1.intersect(bvh2)
#  for ibvh1, ibvh2, ip in ibvhs:
#      print ip
#  ```
class BVH:
    ## Constructor
    def __init__(self, points, level=0):
        self._level = level
        self._bb = BoundingBox(points)
        self._children = []
        self._line = None
        self._createChildren(points)

    ## Return if the node is leaf.
    def isLeaf(self):
        return len(self._children) == 0

    ## Return the points in the node.
    def points(self):
        return self._points

    ## Return the children in the node.
    def children(self):
        if self.isLeaf():
            return [self]

        return self._children

    ## Return true if the given point is included in the node.
    def contains(self, p):
        return self._bb.contains(p)

    ## Find intersections with the given BVH structure.
    def intersect(self, bvh):
        if self._bb.intersects(bvh._bb):
            if bvh.isLeaf() and self.isLeaf():
                ip = self._line.intersect(bvh._line)

                if ip is not None:
                    return [(self, bvh, ip)]

            else:
                ibvhs = []
                for self_ch in self.children():
                    for bvh_ch in bvh.children():
                        ibvh = self_ch.intersect(bvh_ch)
                        if ibvh is not None:
                            ibvhs.extend(ibvh)

                return ibvhs
        else:
            return None
        return None

    ## Plot BVH.
    def plotBVH(self, plt, color="b", alpha=0.05):
        self._bb.plotBoundingBox(plt, color=color, alpha=alpha)
        if self.isLeaf():
            return

        for bvh in self.children():
            bvh.plotBVH(plt, color)

    def _createChildren(self, points):
        if len(points) < 5:
            self._points = points
            self._line = Line(self._points[0], self._points[-1])
            return

        points_left = points[:len(points) / 2 + 1]
        points_right = points[len(points) / 2:]

        self._children = [BVH(points_left, self._level + 1),
                          BVH(points_right, self._level + 1)]


## Implementation of 2D polyline.
class Polyline:
    ## Constructor
    def __init__(self, points):
        self._points = points
        self._bvh = BVH(points)

    ## Return points on the polyline.
    def points(self):
        return self._points

    ## Find intersected points with the given polyline.
    #
    #  BVH structure is used for fast intersection.
    def intersect(self, pl):
        ibvhs = self._bvh.intersect(pl._bvh)
        ips = [ip for ibvh1, ibvh2, ip in ibvhs]
        return ips

    ## Plot polyline.
    def plotPolyline(self, plt):
        ps = self._points
        plt.plot(ps[:, 0], ps[:, 1], "-")

    ## Plot BVH structure.
    def plotBVH(self, plt, color="b"):
        self._bvh.plotBVH(plt, color=color)

    ## Plot intersection with BVH structure.
    def plotIntersection(self, plt,  pl):
        ibvhs = self._bvh.intersect(pl._bvh)

        for ibvh1, ibvh2, ip in ibvhs:
            ibvh1.plotBVH(plt, color="r", alpha=0.2)
            ibvh2.plotBVH(plt, color="r", alpha=0.2)
            plt.plot(ip[0], ip[1], "o", color="r")

        plt.title("Num intersections: %s " % len(ibvhs))


def splinePoints(cvs, num_points=100):
    from scipy.interpolate import UnivariateSpline
    spl = UnivariateSpline(cvs[:, 0], cvs[:, 1])
    bb = BoundingBox(cvs)
    x_new = np.linspace(bb.min()[0], bb.max()[0], num_points)
    y_new = spl(x_new)

    ps = np.zeros((num_points, 2))
    ps[:, 0] = x_new
    ps[:, 1] = y_new
    return ps

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inversetoon.plot.window import showMaximize

    cv1 = np.random.rand(4, 2)
    cv2 = np.random.rand(4, 2)

    ps1 = splinePoints(cv1)
    ps2 = splinePoints(cv2)

    pl1 = Polyline(ps1)
    pl2 = Polyline(ps2)

    pl1.plotPolyline(plt)
    pl2.plotPolyline(plt)

    pl1.plotBVH(plt, color="b")
    pl2.plotBVH(plt, color="g")

    pl1.plotIntersection(plt, pl2)

    showMaximize()