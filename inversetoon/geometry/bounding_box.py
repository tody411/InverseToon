# -*- coding: utf-8 -*-
## @package inversetoon.geometry.bounding_box
#
#  Bounding box class.
#  @author      tody
#  @date        2015/08/12

import numpy as np


## Implementation of a 2D bounding box.
class BoundingBox:
    ## Constructor
    def __init__(self, points=[]):
        self._x_min = np.min(points[:, 0])
        self._x_max = np.max(points[:, 0])

        self._y_min = np.min(points[:, 1])
        self._y_max = np.max(points[:, 1])

    ## Returns the minimum point for the bounding box.
    def min(self):
        return np.array([self._x_min, self._y_min])

    ## Returns the maximum point for the bounding box.
    def max(self):
        return np.array([self._x_max, self._y_max])

    ## Returns the center of the bounding box.
    def center(self):
        return 0.5 * (self.min() + self.max())

    ## Returns true if the bounding box intersects another given bounding box.
    def intersects(self, bb):
        return self._x_max > bb._x_min and self._x_min < bb._x_max and self._y_max > bb._y_min and self._y_min < bb._y_max

    ## Returns true if the bounding box contains the given point.
    def contains(self, p):
        return self._x_min < p[0] and self._x_max > p[0] and self._y_min < p[1] and self._y_max > p[1]

    ## Plot bounding box with matplot.
    def plotBoundingBox(self, plt, **kargs):
        x0, y0 = self.min()
        x1, y1 = self.max()
        points = np.array([(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)])
        plt.fill(points[:, 0], points[:, 1], **kargs)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inversetoon.plot.window import showMaximize

    points = np.random.rand(100, 2)
    plt.scatter(points[:, 0], points[:, 1])
    bb = BoundingBox(points)
    bb.plotBoundingBox(plt)
    showMaximize()