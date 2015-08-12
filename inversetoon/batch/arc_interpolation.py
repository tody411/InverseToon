
# -*- coding: utf-8 -*-
## @package inversetoon.batch.arc_interpolation
#
#  Plot normal cone interpolation error.
#
#  @author      tody
#  @date        2015/08/11

import matplotlib.pyplot as plt

from inversetoon.datasets.isophote import loadData
from inversetoon.batch.batch import isophoteDataSetBatch
from inversetoon.plot.isophote import ScenePlotter, plotSegment
from inversetoon.plot.window import showMaximize
from inversetoon.core.normal_cone import NormalConeInterpolation
from inversetoon.np.norm import normVectors
from inversetoon.core.coloring import colorMap


def datasetFunc(data_name):
    scene = loadData(data_name)
    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    plotter = ScenePlotter(scene, plt)

    plt.title('Arc Interpolation')
    plotter.showNormalImage()

    for isophote_curve in isophote_curves:
        isophote_segments = isophote_curve.toCurveSegments()

        for isophote_segment in isophote_segments:
            normals = isophote_segment.normals()
            N1 = normals[0]
            N2 = normals[-1]
            L = isophote_segment.lightDir()
            parameters = isophote_segment.arcLengthParameters()

            interpolator = NormalConeInterpolation(N1, N2, L)
            normals_interpolated = interpolator.interpolate(parameters)

            normal_error = normVectors(normals_interpolated - normals)
            error_colors = colorMap(normal_error)

            ps = isophote_segment.points()

            plotSegment(plt, ps, error_colors)

    showMaximize()

if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)