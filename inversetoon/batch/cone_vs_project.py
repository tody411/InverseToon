# -*- coding: utf-8 -*-
## @package inversetoon.batch.cone_vs_project
#
#  inversetoon.batch.cone_vs_project utility package.
#  @author      tody
#  @date        2015/08/12

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from inversetoon.batch.batch import isophoteDataSetBatch
from inversetoon.core.normal_cone import NormalConeInterpolation
from inversetoon.core.project_normal_3d import projectTangent3D, projectIteration
from inversetoon.datasets.isophote import loadData
from inversetoon.plot.isophote import ScenePlotter, plotVectors, plotSegment
from inversetoon.plot.window import showMaximize
from inversetoon.core.coloring import scalarToColor, scalarMap, colorNorm
from inversetoon.np.norm import normVectors

from inversetoon.util.logger import getLogger
logger = getLogger(__name__)

def computeData(scene):
    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    data_list = []

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
            #normals_al = arcLengthInterpolation(normals_gt[0], normals_gt[-1], parameters)
            normals_3D = np.array(normals_al)
            tangents_2D = isophote_segment.tangents()
            tangents_3D = projectTangent3D(tangents_2D, normals_3D)

            normals_3D = projectIteration(tangents_3D, normals_3D, parameters, 20)

            ps = isophote_segment.points()

            normals_al_error = normVectors(normals_gt - normals_al)
            normals_3d_error = normVectors(normals_gt - normals_3D)

            data_list.append({"ps": ps,
                              "normals_gt": normals_gt,
                              "normals_al": normals_al,
                              "normals_3D": normals_3D,
                              "normals_al_error": normals_al_error,
                              "normals_3d_error": normals_3d_error})
    return data_list


def datasetFunc(data_name):
    scene = loadData(data_name)
    data_list = computeData(scene)

    plotter = ScenePlotter(scene, plt)

    plt.title('Arc length VS Project 3D')
    plt.subplot(131)
    plt.title('Normal Vectors')
    plotter.showNormalImage()

    legend_gt = ("Ground truth", (1.0, 0.0, 0.0))
    legend_al = ("Arc length", (0.0, 1.0, 0.0))
    legend_3d = ("Project 3D", (0.0, 0.0, 1.0))

    for data in data_list:
        plotVectors(plt, data["ps"], data["normals_gt"], color=legend_gt[1])
        plotVectors(plt, data["ps"], data["normals_al"], color=legend_al[1])
        plotVectors(plt, data["ps"], data["normals_3D"], color=legend_3d[1])

    plt.legend(handles=[mpatches.Patch(color=legend_gt[1], label=legend_gt[0]),
                        mpatches.Patch(color=legend_al[1], label=legend_al[0]),
                        mpatches.Patch(color=legend_3d[1], label=legend_3d[0])])
    error_max = 0.0
    error_min = 0.0
    for data in data_list:
        error_max = np.max([error_max, np.max(data["normals_al_error"])])
        error_max = np.max([error_max, np.max(data["normals_3d_error"])])

    logger.debug("error_range: %s - %s" %(error_min, error_max))

    plt.subplot(132)
    plotter.showNormalImage()
    plt.title('Arc length error')
    for data in data_list:
        error_colors = scalarToColor(data["normals_al_error"], vmin=error_min, vmax=error_max)

        plotSegment(plt, data["ps"], error_colors)

    scalar_map = scalarMap(error_min, error_max)
    scalar_map.set_array([error_min, error_max])
    plt.colorbar(scalar_map)

    plt.subplot(133)
    plotter.showNormalImage()
    plt.title('Project 3D error')
    for data in data_list:
        error_colors = scalarToColor(data["normals_3d_error"], vmin=error_min, vmax=error_max)

        plotSegment(plt, data["ps"], error_colors)

    scalar_map = scalarMap(error_min, error_max)
    scalar_map.set_array([error_min, error_max])
    plt.colorbar(scalar_map)
    showMaximize()


if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)
