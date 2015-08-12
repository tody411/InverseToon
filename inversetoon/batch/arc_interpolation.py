
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
from inversetoon.core.coloring import scalarToColor


def computeData(scene):
    data_list = []

    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    for isophote_curve in isophote_curves:
        isophote_segments = isophote_curve.toCurveSegments()

        for isophote_segment in isophote_segments:
            I = isophote_segment.isoValue()
            I = 2.0 * I - 1.0

            normals_gt = isophote_segment.normals()
            parameters = isophote_segment.arcLengthParameters()
            normals_al = NormalConeInterpolation(normals_gt[0],
                                                 normals_gt[-1],
                                                 isophote_segment.lightDir(),
                                                 I).interpolate(parameters)
            ps = isophote_segment.points()

            normals_error = normVectors(normals_gt - normals_al)

            data_list.append({"ps": ps,
                              "normals_gt": normals_gt,
                              "normals_al": normals_al,
                              "normals_error": normals_error})
    return data_list


def datasetFunc(data_name):
    scene = loadData(data_name)
    data_list = computeData(scene)

    plotter = ScenePlotter(scene, plt)

    plt.title('Arc Interpolation')
    plotter.showNormalImage()

    for data in data_list:
        error_colors = scalarToColor(data["normals_error"])

        plotSegment(plt, data["ps"], error_colors)

    showMaximize()

if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)