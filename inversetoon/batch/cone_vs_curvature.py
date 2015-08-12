# -*- coding: utf-8 -*-
## @package inversetoon.batch.cone_vs_curvature
#
#  inversetoon.batch.cone_vs_curvature utility package.
#  @author      tody
#  @date        2015/08/11

import numpy as np
import matplotlib.pyplot as plt

from inversetoon.datasets.isophote import loadData
from inversetoon.batch.batch import isophoteDataSetBatch
from inversetoon.plot.isophote import ScenePlotter, plotSegment
from inversetoon.plot.window import showMaximize
from inversetoon.core.coloring import scalarToColor, featureTypeColors
from inversetoon.core.smoothing import smoothing


def plotFeatureChanges(plt, ps, feature):
    epsilon = 0.001
    feature_min = np.min(feature)
    feature_max = np.max(feature)
    feature_range = feature_max - feature_min
    ofeature_changes_colors = featureTypeColors(feature,
                                                vmin=-feature_range * epsilon,
                                                vmax=feature_range * epsilon)
    plotSegment(plt, ps, ofeature_changes_colors)


def computeData(scene):
    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    data_list = []

    for isophote_curve in isophote_curves:
        isophote_segments = isophote_curve.toCurveSegments()

        for isophote_segment in isophote_segments:
            curvatures = isophote_segment.curvatures()
            curvatures = smoothing(curvatures, smooth=20.0)

            cone_angle_changes = isophote_segment.coneAngleChanges()
            cone_angle_changes = smoothing(cone_angle_changes, smooth=0.05)

            misclassification = curvatures * cone_angle_changes

            ps = isophote_segment.points()

            data_list.append({"ps": ps,
                              "curvatures": curvatures,
                              "cone_angle_changes": cone_angle_changes,
                              "misclassification": misclassification})
    return data_list


def datasetFunc(data_name):
    scene = loadData(data_name)
    data_list = computeData(scene)

    plotter = ScenePlotter(scene, plt)

    plt.title('Curvature VS Cone Angles')

    plt.subplot(131)
    plotter.showNormalImage()
    plt.title('Curvature')
    for data in data_list:
        plotFeatureChanges(plt, data["ps"], data["curvatures"])

    plt.subplot(132)
    plotter.showNormalImage()
    plt.title('Cone Angles')
    for data in data_list:
        plotFeatureChanges(plt, data["ps"], data["cone_angle_changes"])

    plt.subplot(133)
    plotter.showNormalImage()
    plt.title('Misclassification')
    for data in data_list:
        plotFeatureChanges(plt, data["ps"], data["misclassification"])

    showMaximize()


if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)
