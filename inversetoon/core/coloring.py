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


## Color map function with the matplot cmap.
def colorMap(values, vmin=None, vmax=None, cmap='jet'):
    if vmin is None:
        vmin = np.min(values)

    if vmax is None:
        vmax = np.max(values)

    cNorm = colors.Normalize(vmin=vmin, vmax=vmax)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)

    return scalarMap.to_rgba(values)


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
