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
from inversetoon.results.results import resultDir, resultFile
from inversetoon.core.angle import angleErros
logger = getLogger(__name__)


def computeData(scene):
    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    data_list = []

    for isophote_curve in isophote_curves:
        isophote_segments = isophote_curve.toCurveSegments()

        for isophote_segment in isophote_segments:
            L = isophote_segment.lightDir()
            isophote_segment = isophote_segment.divide(int(0.2 * isophote_segment.numPoints()), int(0.5 * isophote_segment.numPoints()))

            if isophote_segment.numPoints() < 3:
                continue

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

            normals_3D = projectIteration(L, I, tangents_3D, normals_3D, parameters, 40)

            ps = isophote_segment.points()

            normals_al_error = angleErros(normals_gt, normals_al)
            normals_3d_error = angleErros(normals_gt, normals_3D)

            data_list.append({"ps": ps,
                              "normals_gt": normals_gt,
                              "normals_al": normals_al,
                              "normals_3D": normals_3D,
                              "normals_al_error": normals_al_error,
                              "normals_3d_error": normals_3d_error})
    return data_list


def arcVSprojectFigure(scnene_plotter, data_name, segment_id, result_data):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 5))
    font_size = 15
    fig.subplots_adjust(left=0.15, right=0.9, top=0.86, hspace=0.1, wspace=0.05)
    fig.suptitle("Arc-Length Interpolation VS Project 3D", fontsize=font_size)

    plt.subplot(131)
    plt.title('Normal Vectors\n', fontsize=font_size)
    scnene_plotter.showNormalImage()
    plt.axis('off')

    legend_gt = ("Ground Truth", (1.0, 0.0, 0.0))
    legend_al = ("Arc-Length", (0.0, 1.0, 0.0))
    legend_3d = ("Project 3D", (0.0, 0.0, 1.0))

    plotVectors(plt, result_data["ps"], result_data["normals_gt"], color=legend_gt[1], l=70, step=2)
    plotVectors(plt, result_data["ps"], result_data["normals_al"], color=legend_al[1], l=70, step=2)
    plotVectors(plt, result_data["ps"], result_data["normals_3D"], color=legend_3d[1], l=70, step=2)

    plt.legend(bbox_to_anchor=(0.2, 1), handles=[mpatches.Patch(color=legend_gt[1], label=legend_gt[0]),
                        mpatches.Patch(color=legend_al[1], label=legend_al[0]),
                        mpatches.Patch(color=legend_3d[1], label=legend_3d[0])])
    error_max = 30.0
    error_min = 0.0

    plt.subplot(132)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Arc-Length Error\n %5.2f $^\circ$' %np.average(result_data["normals_al_error"]), fontsize=font_size)
    error_colors = scalarToColor(result_data["normals_al_error"], vmin=error_min, vmax=error_max)
    plotSegment(plt, result_data["ps"], error_colors)

    plt.subplot(133)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Project 3D Error\n %5.2f $^\circ$' %np.average(result_data["normals_3d_error"]), fontsize=font_size)
    error_colors = scalarToColor(result_data["normals_3d_error"], vmin=error_min, vmax=error_max)
    plotSegment(plt, result_data["ps"], error_colors)

    ax_colorbar = fig.add_axes([0.9, 0.15, 0.03, 0.7])

    scalar_map = scalarMap(error_min, error_max)
    scalar_map.set_array([error_min, error_max])
    fig.colorbar(scalar_map, cax=ax_colorbar)

    result_name = "arc_vs_project"
    result_dir = resultDir(result_name)

    result_file = resultFile(result_dir, data_name + "_%s" % segment_id)
    plt.savefig(result_file, transparent=True)


def resultDataFunc(scnene_plotter, data_name, segment_id, result_data):
    if len(result_data["ps"]) < 30:
        return

    arcVSprojectFigure(scnene_plotter, data_name, segment_id, result_data)


def datasetFunc(data_name):
    scene = loadData(data_name)
    result_data_list = computeData(scene)

    scnene_plotter = ScenePlotter(scene, plt)

    for i, result_data in enumerate(result_data_list):
        resultDataFunc(scnene_plotter, data_name, i, result_data)

if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)
