# -*- coding: utf-8 -*-
## @package inversetoon.geometry.bounding_box
#
#  Implementation of a 3D bounding box.
#  @author      tody
#  @date        2015/08/12

import numpy as np


## Implementation of a 2D bounding box.
class BoundingBox:
    ## Constructor
    #
    #  @param points (n x 2) array.
    def __init__(self, points=[]):
        if len(points) > 0:
            self.create(points)

    ## Creates the bounding box which contains the given points.
    #
    #  @param points (n x 2) array.
    def create(self, points):
        points = np.array(points)
        xs, ys = points[:, 0], points[:, 1]
        self._x_min = np.min(xs)
        self._x_max = np.max(xs)

        self._y_min = np.min(ys)
        self._y_max = np.max(ys)

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
        x, y = p
        return self._x_min < x and self._x_max > x and self._y_min < y and self._y_max > y

    ## Plot bounding box with matplot.
    def plotBoundingBox(self, plt, color="b", alpha=0.05, **kargs):
        x0, y0 = self.min()
        x1, y1 = self.max()
        points = np.array([(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)])
        plt.fill(points[:, 0], points[:, 1], color=color, alpha=alpha, **kargs)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inversetoon.plot.window import showMaximize

    points = np.random.rand(100, 2)
    plt.scatter(points[:, 0], points[:, 1])
    bb = BoundingBox(points)
    bb.plotBoundingBox(plt)
    showMaximize()