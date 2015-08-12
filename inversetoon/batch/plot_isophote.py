# -*- coding: utf-8 -*-
## @package inversetoon.batch.plot_isophote
#
#  Isophote plotting functions.
#  @author      tody
#  @date        2015/07/31

import matplotlib.pyplot as plt

from inversetoon.datasets.isophote import loadData
from inversetoon.batch.batch import isophoteDataSetBatch
from inversetoon.plot.isophote import ScenePlotter
from inversetoon.plot.window import showMaximize


def datasetFunc(data_name):
    scene = loadData(data_name)

    plotter = ScenePlotter(scene, plt)
    silhouette_plotter = plotter.silhouettePlotter()

    plt.title('Isophote Scene')
    plotter.showNormalImage()
    #silhouette_plotter.plotCVs()
    silhouette_plotter.plotNormalVectors()
    silhouette_plotter.plotCurves(color=(0.1, 0.5, 0.1))

    for isophote_plotter in plotter.isophotePlotters():
        #isophote_plotter.plotCVs()
        isophote_plotter.plotCurves(color=(0.1, 0.1, 0.3))
        isophote_plotter.plotNormalVectors(color=(0.1, 0.1, 0.3), step=5)
    showMaximize()


if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)