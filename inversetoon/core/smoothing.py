# -*- coding: utf-8 -*-
## @package inversetoon.core.smoothing
#
#  Smoothing functions.
#  @author      tody
#  @date        2015/08/11

import numpy as np
from scipy.interpolate import UnivariateSpline

from inversetoon.np.norm import isVector


def _smoothing_1D(y, x, smooth):
    if len(y) < 5:
        return y
    spl = UnivariateSpline(x, y, s=smooth)
    return spl(x)


def smoothing(y, x=None, smooth=None):
    if x is None:
        x = np.linspace(0.0, 1.0, len(y))

    if isVector(y):
        return _smoothing_1D(y, x, smooth)

    y_smooth = np.array(y)

    dimension = y.shape[1]

    for di in range(dimension):
        y_smooth[:, di] = _smoothing_1D(y[:, di], x, smooth)
    return y_smooth


def smoothing_contour(contour):
    segments = contour.segments()

    segments_smooth = []
    for segment in segments:
        segments_smooth.append(smoothing(segment))

    contour.setSegments(segments_smooth)

    return contour
