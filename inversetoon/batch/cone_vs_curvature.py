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
from inversetoon.plot.isophote import ScenePlotter, plotSegment, plotVectors, plotNormalColors
from inversetoon.plot.window import showMaximize
from inversetoon.core.coloring import scalarToColor, featureTypeColors, scalarMap
from inversetoon.core.smoothing import smoothing
from inversetoon.results.results import resultDir, resultFile
from inversetoon.core.normal_cone import NormalConeInterpolation
from inversetoon.np.norm import normVectors
from inversetoon.core.angle import angleErros


def plotFeatureChanges(plt, ps, feature):
    epsilon = 0.001
    feature_min = np.min(feature)
    feature_max = np.max(feature)
    feature_range = feature_max - feature_min
    ofeature_changes_colors = featureTypeColors(feature,
                                                vmin=-feature_range * epsilon,
                                                vmax=feature_range * epsilon)
    plotSegment(plt, ps, ofeature_changes_colors)


def clipSegments(segment_points, bool_array):
    clipped_segments = []

    clipped_segment = []
    for p, b in zip(segment_points, bool_array):
        if b:
            clipped_segment.append(p)
        else:
            if len(clipped_segment) > 0:
                clipped_segments.append(np.array(clipped_segment))
                clipped_segment = []

    if len(clipped_segment) > 0:
        clipped_segments.append(np.array(clipped_segment))
    return clipped_segments


def rescaleCurvature(curvatures, cone_angle_range):
    curvature_range = [curvatures[0], curvatures[-1]]

    curvatures_scaled = (curvatures - curvature_range[0]) / (curvature_range[1] - curvature_range[0])
    curvatures_scaled = (cone_angle_range[1] - cone_angle_range[0]) * curvatures_scaled + cone_angle_range[0]
    return curvatures_scaled


def computeData(scene):
    isophote_mesh = scene.isophoteMesh()
    isophote_curves = isophote_mesh.isophoteCurves()

    data_list = []

    for isophote_curve in isophote_curves:
        isophote_segments = isophote_curve.toCurveSegments()

        for isophote_segment in isophote_segments:
            isophote_segment = isophote_segment.divide(int(0.2 * isophote_segment.numPoints()), int(0.5 * isophote_segment.numPoints()))

            if isophote_segment.numPoints() < 3:
                continue

            I = isophote_segment.isoValue()
            I = 2.0 * I - 1.0

            curvatures = isophote_segment.curvatures()
            curvatures = smoothing(curvatures, smooth=15.0)
            curvatures = curvatures / np.max(np.abs(curvatures))

            normals_gt = isophote_segment.normals()
            parameters = isophote_segment.arcLengthParameters()

            normals_al = NormalConeInterpolation(normals_gt[0],
                                                 normals_gt[-1],
                                                 isophote_segment.lightDir(),
                                                 I).interpolate(parameters)

            normals_al_error = angleErros(normals_gt, normals_al)

            cone_angle_changes = isophote_segment.coneAngleChanges()
            cone_angle_changes = smoothing(cone_angle_changes, smooth=0.05)
            cone_angle_changes = cone_angle_changes / np.max(np.abs(cone_angle_changes))

            misclassification = curvatures * cone_angle_changes

            ps = isophote_segment.points()

            misclassification_segments = clipSegments(ps, misclassification < 0)
            num_misclassification = len(np.where(misclassification < 0)[0])

            misclassification_rate = float(num_misclassification) / float(len(misclassification))

            data_list.append({"ps": ps,
                              "curvatures": curvatures,
                              "cone_angle_changes": cone_angle_changes,
                              "misclassification_segments": misclassification_segments,
                              "misclassification_rate": misclassification_rate,
                              "normals_gt": normals_gt,
                              "normals_al": normals_al,
                              "normals_al_error": normals_al_error})
    return data_list


def curvatureVSconeAnglesFigure(scnene_plotter, data_name, segment_id, result_data):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 5))
    font_size = 15
    fig.subplots_adjust(left=0.05, right=0.95, top=0.86, hspace=0.1, wspace=0.05)
    fig.suptitle("Curvature VS Cone Angle", fontsize=font_size)

    plt.subplot(131)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Curvature\n', fontsize=font_size)
    plotFeatureChanges(plt, result_data["ps"], result_data["curvatures"])

    plt.subplot(132)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Cone Angle\n', fontsize=font_size)
    plotFeatureChanges(plt, result_data["ps"], result_data["cone_angle_changes"])

    plt.subplot(133)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Misclassification\n%5.1f %%' % (100 * result_data["misclassification_rate"]), fontsize=font_size)

    for segment in result_data["misclassification_segments"]:
        plotSegment(plt, segment, color=(0.8, 0.2, 0.2))

    result_name = "cone_vs_curvature/misclassification"
    result_dir = resultDir(result_name)

    result_file = resultFile(result_dir, data_name + "_%s" % segment_id)
    plt.savefig(result_file, transparent=True)


def curvatureVSconeAnglesSignal(scnene_plotter, data_name, segment_id, result_data):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 5))
    font_size = 15
    fig.subplots_adjust(left=0.05, right=0.9, top=0.86, hspace=0.1, wspace=0.05)
    fig.suptitle("Curvature VS Cone Angle", fontsize=font_size)

    plt.subplot(131)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Curvature', fontsize=font_size)
    curvature_colors = scalarToColor(result_data["curvatures"], vmin=-1.0, vmax=1.0)
    plotSegment(plt, result_data["ps"], curvature_colors)

    plt.subplot(132)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Cone Angle', fontsize=font_size)
    cone_colors = scalarToColor(result_data["cone_angle_changes"], vmin=-1.0, vmax=1.0)
    plotSegment(plt, result_data["ps"], cone_colors)

    plt.subplot(133)
    plt.title('Signals', fontsize=font_size)
    xs = np.arange(len(result_data["curvatures"]))
    curvatures = result_data["curvatures"]
    cone_angle_changes = result_data["cone_angle_changes"]
    rescaled_curvatures = rescaleCurvature(curvatures, [cone_angle_changes[0], cone_angle_changes[-1]])
    plt.plot(xs, curvatures, label='Curvature')
    plt.plot(xs, cone_angle_changes, label='Cone Angle')
    # plt.plot(xs, rescaled_curvatures, label='Rescaled Curvatures')
    plt.legend()

    result_name = "cone_vs_curvature/signal"
    result_dir = resultDir(result_name)

    result_file = resultFile(result_dir, data_name + "_%s" % segment_id)
    plt.savefig(result_file, transparent=True)


def curvatureVSconeAnglesNormal(scnene_plotter, data_name, segment_id, result_data):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 5))
    font_size = 15
    fig.subplots_adjust(left=0.05, right=0.9, top=0.86, hspace=0.1, wspace=0.05)
    fig.suptitle("Arc-Length Interpolation", fontsize=font_size)

    plt.subplot(131)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Ground Truth\n', fontsize=font_size)
    plotSegment(plt, result_data["ps"], color=(0.5, 0.1, 0.1))
    # plotVectors(plt, result_data["ps"], result_data["normals_gt"], step=5)

    plt.subplot(132)
    scnene_plotter.showNormalImage()
    plt.axis('off')
    plt.title('Interpolated Normal\n', fontsize=font_size)
    plotNormalColors (plt, result_data["ps"], result_data["normals_al"])

    plt.subplot(133)
    plt.title('Interpolation Error\n %4.1f $^\circ$' % np.max(result_data["normals_al_error"]), fontsize=font_size)
    scnene_plotter.showNormalImage()
    plt.axis('off')

    error_min = 0.0
    error_max = 30.0
    #error_max = np.max([0.0, np.max(result_data["normals_al_error"])])
    error_colors = scalarToColor(result_data["normals_al_error"], vmin=error_min, vmax=error_max)
    plotSegment(plt, result_data["ps"], error_colors)

    ax_colorbar = fig.add_axes([0.9, 0.15, 0.03, 0.7])

    scalar_map = scalarMap(error_min, error_max)
    scalar_map.set_array([error_min, error_max])
    fig.colorbar(scalar_map, cax=ax_colorbar)

    result_name = "cone_vs_curvature/normal"
    result_dir = resultDir(result_name)

    result_file = resultFile(result_dir, data_name + "_%s" % segment_id)
    plt.savefig(result_file, transparent=True)


def resultDataFunc(scnene_plotter, data_name, segment_id, result_data):
    if len(result_data["ps"]) < 30:
        return

    # curvatureVSconeAnglesNormal(scnene_plotter, data_name, segment_id, result_data)
    # curvatureVSconeAnglesFigure(scnene_plotter, data_name, segment_id, result_data)
    curvatureVSconeAnglesSignal(scnene_plotter, data_name, segment_id, result_data)


def datasetFunc(data_name):
    scene = loadData(data_name)
    result_data_list = computeData(scene)

    scnene_plotter = ScenePlotter(scene, plt)

    for i, result_data in enumerate(result_data_list):
        resultDataFunc(scnene_plotter, data_name, i, result_data)


if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)
