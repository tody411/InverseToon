import os
import numpy as np

import normal

from inversetoon.util.logger import getLogger
import inversetoon.core.shader.toon as toon
from inversetoon.util.timer import timing_func
from inversetoon.cv.image import setAlpha, to32F
logger = getLogger(__name__)


## Load data for the data name.
@timing_func
def loadData(data_name, L,
             borders=[0.5, 0.8],
             colors=[np.array([0.2, 0.2, 0.5]), np.array([0.3, 0.3, 0.6]), np.array([0.5, 0.5, 0.8])]):

    N_32F, A_8U = normal.loadData(data_name)
    C_32F = toon.diffuse(N_32F, L, borders, colors)

    C_32F = setAlpha(C_32F, to32F(A_8U))
    return C_32F

