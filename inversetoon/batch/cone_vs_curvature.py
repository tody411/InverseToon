# -*- coding: utf-8 -*-
## @package inversetoon.batch.cone_vs_curvature
#
#  inversetoon.batch.cone_vs_curvature utility package.
#  @author      tody
#  @date        2015/08/11

import matplotlib.pyplot as plt

from inversetoon.datasets.isophote import loadData
from inversetoon.batch.batch import isophoteDataSetBatch
from inversetoon.plot.isophote import ScenePlotter, plotSegment
from inversetoon.plot.window import showMaximize
from inversetoon.core.coloring import colorMap, featureTypeColors
from inversetoon.core.smoothing import smoothing


def plotConeAngleSegmentation(data_name):
    pass


def plotCurvatureSegmentation(data_name):
    scene = loadData(data_name)
    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    plotter = ScenePlotter(scene, plt)

    plt.title('Curvature segmentation')
    plotter.showNormalImage()

    for isophote_curve in isophote_curves:
        isophote_segments = isophote_curve.toCurveSegments()

        for isophote_segment in isophote_segments:
            curvatures = isophote_segment.curvatures()
            curvatures = smoothing(curvatures, smooth=20.0)

            ps = isophote_segment.points()
            curvature_colors = featureTypeColors(curvatures, vmin=-0.005, vmax=0.005)

            plotSegment(plt, ps, curvature_colors)

    showMaximize()


def datasetFunc(data_name):
    pass

if __name__ == '__main__':
    isophoteDataSetBatch(plotCurvatureSegmentation)
