# -*- coding: utf-8 -*-
## @package inversetoon.batch.coloring
#
#  Coloring functions.
#  @author      tody
#  @date        2015/08/11

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


def colorNorm(vmin, vmax):
    c_norm = colors.Normalize(vmin=vmin, vmax=vmax)
    return c_norm


## Scalar map function for the target min, max values.
def scalarMap(vmin, vmax, cmap='jet'):
    c_norm = colorNorm(vmin=vmin, vmax=vmax)
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=cmap)
    return scalar_map


## Color map function for the input scalar values.
def scalarToColor(values, vmin=None, vmax=None, cmap='jet'):
    if vmin is None:
        vmin = np.min(values)

    if vmax is None:
        vmax = np.max(values)

    scalar_map = scalarMap(vmin, vmax, cmap)

    return scalar_map.to_rgba(values)


def featureTypeColors(values, vmin=None, vmax=None,
                      cmin=np.array([0.0, 0.0, 1.0]), cmid=np.array([0.0, 1.0, 0.0]), cmax=np.array([1.0, 0.0, 0.0])):
    t = 0.3
    if vmin is None:
        vmin = (1.0 - t) * np.min(values) + t * np.max(values)

    if vmax is None:
        vmax = (1.0 - t) * np.max(values) + t * np.min(values)

    cs = np.zeros((len(values), 3))
    cs[:] = cmid

    cs[values < vmin] = cmin
    cs[values > vmax] = cmax
    return cs
