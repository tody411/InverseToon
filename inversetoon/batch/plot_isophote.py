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
    plt.subplot(121)
    plt.title('Normal')
    plotter.showNormalImage()

    plt.subplot(122)
    plt.title('Alpha')
    plotter.showAlphaImage()
    #silhouette_plotter.plotCVs()
    silhouette_plotter.plotNormalVectors()
    silhouette_plotter.plotCurves()
    showMaximize()




if __name__ == '__main__':
    isophoteDataSetBatch(datasetFunc)