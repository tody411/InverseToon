

# -*- coding: utf-8 -*-
## @package inversetoon.plot.isophote
#
#  Isophote plotting functions.
#  @author      tody
#  @date        2015/07/31

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from inversetoon.io.image import loadRGBA


## Plot 2D vectors as arrows.
def plotVectors(plt, ps, vectors, color=(1.0, 0.0, 0.0), l=40):
    for p, v in zip(ps, vectors):
        lv = l * v[:2]
        plt.arrow(p[0], p[1], lv[0], - lv[1],
                  head_width=0.05 * l, head_length=0.1 * l, fc=color, ec=color)


## Plot segment data as polylines.
def plotSegment(plt, segment, color=(0.1, 0.1, 0.3), linewidth=2, **kargs):
#     line_segments = LineCollection([segment], linewidths=linewidth,
#                                 colors=color, linestyle='solid')
#     plt.add_collection(line_segments)

    if not isinstance(color[0], float):
        for si in range(len(segment))[:-1]:
            plt.plot(segment[si:si + 2, 0], segment[si:si + 2, 1],
                     "-", color=color[si], linewidth=linewidth, **kargs)

    else:
        plt.plot(segment[:, 0], segment[:, 1], "-", color=color, linewidth=linewidth, **kargs)




## Curve plotter.
class CurvePlotter:
    ## Constructor
    def __init__(self, curve, plt):
        self._curve = curve
        self._plt = plt

    def setSilhouette(self, silhouette):
        self._curve = silhouette

    def setPlotter(self, plt):
        self._plt = plt

    ## Plot control vertices.
    def plotCVs(self, color=(0.8, 0.3, 0.3), size=40, **kargs):
        ps = self._curve.CVs()
        self._plt.scatter(ps[:, 0], ps[:, 1], c=color, s=size, **kargs)

    ## Plot normal vectors.
    def plotNormalVectors(self, color=(1.0, 0.0, 0.0), l=40, step=3):
        ps = self._curve.CVs()[::step]
        ns = self._curve.normals()[::step]

        plotVectors(self._plt, ps, ns, color, l)

    ## Plot curves.
    def plotCurves(self, color=(0.1, 0.1, 0.3), linewidth=2):
        segments_cvIDs = self._curve.segmentsCVIDs()
        ps = self._curve.CVs()

        for segment_cvIDs in segments_cvIDs:
            segment = ps[segment_cvIDs]
            plotSegment(self._plt, segment, color, linewidth)


## Isophote scene plotter.
#  Attributes:
#  * scene: Scene data.
#  * plt: Matplot plotter.
class ScenePlotter:
    ## Constructor
    def __init__(self, scene, plt):
        self._scene = scene
        self._plt = plt

    def setScene(self, scene):
        self._scene = scene

    def setPlotter(self, plt):
        self._plt = plt

    def showNormalImage(self):
        normal_image = loadRGBA(self._scene.normalImageFile())
        img_plot = self._plt.imshow(normal_image)
        self._plt.xlim([0, normal_image.shape[1]])
        self._plt.ylim([normal_image.shape[0], 0])
        return img_plot

    def showAlphaImage(self):
        alpha_image = self._scene.alphaImage()
        img_plot = self._plt.imshow(alpha_image, cmap=plt.cm.gray)
        self._plt.xlim([0, alpha_image.shape[1]])
        self._plt.ylim([alpha_image.shape[0], 0])
        return img_plot

    def silhouettePlotter(self):
        return CurvePlotter(self._scene.isophoteMesh().silhouetteCurve(), self._plt)

    def isophotePlotter(self, isophote_id):
        isophote = self._scene.isophoteMesh().isophoteCurves()[isophote_id]
        return CurvePlotter(isophote, self._plt)

    def isophotePlotters(self):
        plotters = []
        for isophote in self._scene.isophoteMesh().isophoteCurves():
            plotters.append(CurvePlotter(isophote, self._plt))
        return plotters
