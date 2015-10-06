
import numpy as np
import matplotlib.pyplot as plt

import inversetoon.datasets.normal as normal
import inversetoon.datasets.diffuse as diffuse
import inversetoon.datasets.toon as toondata
import inversetoon.core.shader.lambert as lambert
from inversetoon.cv.light import lightSphere
from inversetoon.np.norm import normalizeVector
from inversetoon.cv.image import luminance, to32F
from inversetoon.core.silhouette import silhoutteCurve, silhouetteNormal
from inversetoon.plot.window import showMaximize
from inversetoon.results.results import resultDir, resultFile
from inversetoon.core.angle import angleError


def showLightSphere(plt, L):
    I_32F = lightSphere(L)
    plt.imshow(I_32F)


def estimateResultFunc(data_name, target_name,
                       N_32F, L_g, I_32F, A_8U,
                       method_name, estimate_func):
    L_g = normalizeVector(L_g)
    silhouette_curve, S_8U = silhoutteCurve(A_8U)
    N_sil = silhouetteNormal(A_8U)
    silhouette_curve.setNormalImage(N_sil)

    N_sil = silhouette_curve.normals()

    cvs_sil = silhouette_curve.CVs()

    I_sil = np.array([I_32F[cv[1], cv[0]] for cv in cvs_sil])

    input_data = {"N_sil": N_sil, "I_sil": I_sil,
                  "cvs_sil": cvs_sil, "I": I_32F, "A": A_8U}

    fig = plt.figure(figsize=(8, 8))
    fig.suptitle("Light estimation: %s" % method_name)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.82, wspace=0.02, hspace=0.4)

    plt.subplot(2, 2, 1)
    plt.title("Ground truth")
    showLightSphere(plt, L_g)
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.title("Illumination")

    A_32F = to32F(A_8U)
    I_org = I_32F * A_32F
    plt.gray()
    plt.imshow(I_org)
    plt.axis('off')

    output_data = estimate_func(input_data)
    L = output_data["L"]
    L = normalizeVector(L)
    L_error = angleError(L_g, L)
    plt.subplot(2, 2, 3)
    plt.title("Estimated error\n %4.1f $^\circ$" % L_error)
    showLightSphere(plt, L)
    plt.axis('off')

    I_est = lambert.diffuse(N_32F, L) * A_32F
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
