
import numpy as np
import matplotlib.pyplot as plt

import inversetoon.datasets.normal as normal
import inversetoon.datasets.diffuse as diffuse
import inversetoon.datasets.toon as toondata
import inversetoon.core.shader.lambert as lambert
from inversetoon.cv.light import lightSphere
from inversetoon.np.norm import normalizeVector
from inversetoon.cv.image import luminance
from inversetoon.core.silhouette import silhoutteCurve, silhouetteNormal
from inversetoon.plot.window import showMaximize
from inversetoon.results.results import resultDir, resultFile


def showLightSphere(plt, L):
    I_32F = lightSphere(L)
    plt.imshow(I_32F)


def estimateResultFunc(data_name, target_name,
                       N_32F, L_g, I_32F, A_8U,
                       method_name, estimate_func):
    print L_g
    silhouette_curve, S_8U = silhoutteCurve(A_8U)
    N_sil = silhouetteNormal(A_8U)
    silhouette_curve.setNormalImage(N_sil)

    Ns = silhouette_curve.normals()

    cvs = silhouette_curve.CVs()

    Is = np.array([I_32F[cv[1], cv[0]] for cv in cvs])

    fig = plt.figure(figsize=(8, 8))
    fig.suptitle("Light estimation: %s" % method_name)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.82, wspace=0.02, hspace=0.3)

    plt.subplot(2, 2, 1)
    plt.title("Ground truth: %s" % L_g)
    showLightSphere(plt, L_g)
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.title("Illumination")

    plt.gray()
    plt.imshow(I_32F)
    plt.axis('off')

    L, error = estimate_func(Ns, Is)
    plt.subplot(2, 2, 3)
    plt.title("Estimated: %s\n%s" % (L, error))
    showLightSphere(plt, L)
    plt.axis('off')

    I_est = lambert.diffuse(N_32F, L)
    plt.subplot(2, 2, 4)
    plt.gray()
    plt.imshow(I_est)
    plt.axis('off')

    result_dir = resultDir("LightEstimation/%s" %data_name)
    result_file = resultFile(result_dir, "%s_%s" %(target_name, method_name))
    plt.savefig(result_file)


def testDiffuse(method_name, estimate_func):
    L_g = normalizeVector(np.array([-0.5, 0.7, 0.5]))
    for data_name in normal.dataNames():
        N_32F, A_8U = normal.loadData(data_name)
        I_32F, A_8U = diffuse.loadData(data_name, L_g)
        estimateResultFunc(data_name, "Lambert", N_32F, L_g, I_32F, A_8U, method_name, estimate_func)


def testToon(method_name, estimate_func):
    L_g = normalizeVector(np.array([-0.5, 0.7, 0.5]))

    for data_name in normal.dataNames():
        N_32F, A_8U = normal.loadData(data_name)
        C_32F = toondata.loadData(data_name, L_g)

        I_32F = luminance(C_32F[:, :, :3])
        estimateResultFunc(data_name, "Toon", N_32F, L_g, I_32F, A_8U, method_name, estimate_func)
