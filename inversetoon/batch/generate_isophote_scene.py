# -*- coding: utf-8 -*-
## @package inversetoon.batch.generate_isophote_scene
#
#  Isophote scene generator.
#  @author      tody
#  @date        2015/07/31

import numpy as np

from inversetoon.batch.batch import normalDataSetBatch
from inversetoon.core.silhouette import silhoutteCurve
from inversetoon.io.image import loadNormal
from inversetoon.core.isophote import isophoteCurves
from inversetoon.cv.light import computeIllumination
from inversetoon.data.isophote_mesh import IsophoteMesh
from inversetoon.data.scene import Scene
from inversetoon.io.isophote import saveSceneData

from inversetoon import datasets


def computeIsophoteCurves(N_32F, L, S_8U):
    I_32F = computeIllumination(N_32F, L)

    isophotes = isophoteCurves(I_32F, M_8U=S_8U)

    for isophote in isophotes:
        isophote.setNormalImage(N_32F)
        isophote.setLightDir(L)

    return I_32F, isophotes


def normalToIsophoteFile(normal_file, scene_file, L1=np.array([-0.5, 0.5, 0.2]), L2=np.array([0.5, 0.5, 0.2])):
    N_32F, A_8U = loadNormal(normal_file)

    silhoutte_curve, S_8U = silhoutteCurve(A_8U)
    silhoutte_curve.setNormalImage(N_32F)

    I1_32F, isophotes1 = computeIsophoteCurves(N_32F, L1, S_8U)
    I2_32F, isophotes2 = computeIsophoteCurves(N_32F, L2, S_8U)

    isophote_curves = []
    isophote_curves.extend(isophotes1)
    isophote_curves.extend(isophotes2)
    isophote_mesh = IsophoteMesh(silhoutte_curve, isophote_curves)

    scene = Scene(isophote_mesh, normal_file)
    saveSceneData(scene_file, scene)


def datasetFunc(data_name):
    normal_file = datasets.normal.dataFile(data_name)
    scene_file = datasets.isophote.dataFile(data_name)

    normalToIsophoteFile(normal_file, scene_file)

if __name__ == '__main__':
    normalDataSetBatch(datasetFunc)
