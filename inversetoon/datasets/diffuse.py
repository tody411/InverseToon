

import os
import numpy as np

import normal

from inversetoon.util.logger import getLogger
import inversetoon.core.shader.lambert as lambert
from inversetoon.util.timer import timing_func
logger = getLogger(__name__)


## Load data for the data name.
@timing_func
def loadData(data_name, L=np.array([0, 0, 1])):
    N_32F, A_8U = normal.loadData(data_name)
    I_32F = lambert.diffuse(N_32F, L)
    return I_32F, A_8U

