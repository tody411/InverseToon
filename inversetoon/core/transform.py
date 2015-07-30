
# -*- coding: utf-8 -*-
## @package inversetoon.core.transform
#
#  Transform utility package.
#  @author      tody
#  @date        2015/07/30

import numpy as np

epsilon = 1e-10


def rotateVector(a, x, cos_t, sin_t):
    p = np.dot(a, x) * a
    q = x - p

    r = np.cross(x, a)
    x_new = p + cos_t * q + sin_t * r
    return x_new


def rotationFromVectors(v_from, v_to):
    a = np.cross(v_to, v_from)
    sin_t = np.linalg.norm(a)
    cos_t = np.dot(v_from, v_to)

    return a, cos_t, sin_t


## Obtain a coordinate frame for the target vector.
def coordinateFrame(v):
    x_axis = np.array([1, 0, 0])
    y_axis = np.array([0, 1, 0])
    z_axis = np.array([0, 0, 1])

    v_x = x_axis
    v_y = y_axis

    a, cos_t, sin_t = rotationFromVectors(z_axis, v)

    print a, cos_t, sin_t

    if sin_t > epsilon:
        v_x = rotateVector(a, x_axis, cos_t, sin_t)
        v_y = rotateVector(a, y_axis, cos_t, sin_t)

    return np.array([v_x, v_y, v])
