# -*- coding: utf-8 -*-
## @package inversetoon.core.intersect
#
#  Polyline intersection via internal subdivision.
#  @author      tody
#  @date        2015/08/12

import numpy as np
from scipy.interpolate import UnivariateSpline

import matplotlib.pyplot as plt
from inversetoon.plot.window import showMaximize

def boundingBox(ps):
    x_min = np.min(ps[:, 0])
    x_max = np.max(ps[:, 0])

    y_min = np.min(ps[:, 1])
    y_max = np.max(ps[:, 1])

    return (x_min, x_max, y_min, y_max)


def boundingBoxIntersect(bb1, bb2):
    return bb1[1] > bb2[0] and bb1[0] < bb2[1] and bb1[3] > bb2[2] and bb1[2] < bb2[3]


def lineEquation(p1, p2):
    peq1 = np.array([p1[0],p1[1],1])
    peq2 = np.array([p2[0],p2[1],1])
    return np.cross(peq1, peq2)


def lineIntersect(l1, l2):
    leq1 = lineEquation(l1[0], l1[1])
    leq2 = lineEquation(l2[0], l2[1])
    ipeq = np.cross(leq1, leq2)

    if np.abs(ipeq[2]) > 0.0001:
        ipeq *= 1.0 / ipeq[2]

    ip = np.array([ipeq[0], ipeq[1]])

    return ip

def polylineIntersect(ps1, ps2):
    num_segment_points = 5
    ps1_list = [ps1[i: i + num_segment_points+1] for i in range(0, len(ps1), num_segment_points)]
    ps2_list = [ps2[i: i + num_segment_points+1] for i in range(0, len(ps2), num_segment_points)]
    intersect_points, bb1_list, bb2_list = np.array(polylineIntersectIter(ps1_list, ps2_list))

    return intersect_points, bb1_list, bb2_list


def polylineIntersectIter(ps1_list, ps2_list):
    bb1_list = [boundingBox(ps1) for ps1 in ps1_list]
    bb2_list = [boundingBox(ps2) for ps2 in ps2_list]

    intersect_points = []

    for ps1, bb1 in zip(ps1_list, bb1_list):
        for ps2, bb2 in zip(ps2_list, bb2_list):

            if boundingBoxIntersect(bb1, bb2):
                ip = lineIntersect([ps1[0], ps1[-1]], [ps2[0], ps2[-1]])
                intersect_points.append(ip)
                continue

    return np.array(intersect_points), bb1_list, bb2_list


def splinePoints(cvs, num_points=100):
    spl = UnivariateSpline(cvs[:, 0], cvs[:, 1])
    bb = boundingBox(cvs)
    x_new = np.linspace(bb[0], bb[1], num_points)
    y_new = spl(x_new)

    ps = np.zeros((num_points, 2))
    ps[:, 0] = x_new
    ps[:, 1] = y_new
    return ps


def plotBoundingBox(bb):
    bb_points = [(bb[0],bb[2]), (bb[0], bb[3]), (bb[1], bb[3]), (bb[1], bb[2]), (bb[0], bb[2])]
    bb_points = np.array(bb_points)

    plt.plot(bb_points[:, 0], bb_points[:, 1], "-")

def testIntersection():
    #cv1 = np.array([(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)])
    #cv2 = np.array([(0.0, 1.0), (1.0, 0.0), (2.0, 2.0), (3.0, 3.0)])

    cv1 = np.random.rand(4, 2)
    cv2 = np.random.rand(4, 2)

    ps1 = splinePoints(cv1)
    ps2 = splinePoints(cv2)

    plt.plot(ps1[:, 0], ps1[:, 1], "-")
    plt.plot(ps2[:, 0], ps2[:, 1], "-")

    intersect_points, bb1_list, bb2_list = polylineIntersect(ps1, ps2)

    for bb1, bb2 in zip(bb1_list, bb2_list):
        plotBoundingBox(bb1)
        plotBoundingBox(bb2)

    print intersect_points
    print "num_intersects: %s" %len(intersect_points)

    if len(intersect_points) > 0:
        plt.plot(intersect_points[:, 0], intersect_points[:, 1], "o")
    showMaximize()

if __name__ == '__main__':
    testIntersection()