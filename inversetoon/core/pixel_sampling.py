# -*- coding: utf-8 -*-
## @package inversetoon.core.pixel_sampling
#
#  inversetoon.core.pixel_sampling utility package.
#  @author      tody
#  @date        2015/10/01

import numpy as np
from inversetoon.cv.image import to32F


## Implementation of pixel sampling.
#
#  input image is automatically converted into np.float32 format.
class PixelSampling:
    ## Constructor
    #  @param image          input image.
    #  @param num_pixels     target number of pixels from the image.
    def __init__(self, image, num_pixels=1000):
        self._image = to32F(image)
        self._num_pixels = num_pixels
        self._pixels = None
        self._coords = None
        self._computeCoordinates()
        self._pixels = self._image2pixels(image)

    ## Pixels.
    def pixels(self):
        return self._pixels

    ## Coordinates.
    def coordinates(self):
        return self._coords

    def _computeCoordinates(self):

        h, w = self._image.shape[:2]
        xs = np.random.randint(w, size=self._num_pixels)
        ys = np.random.randint(h, size=self._num_pixels)

        coords = np.array([xs, ys]).T

        self._coords = coords

    def _image2pixels(self, image):
        if _isGray(image):
            return image[self._coords[:, 1], self._coords[:, 0]]

        return image[self._coords[:, 1], self._coords[:, 0], :]


def _isGray(image):
    return len(image.shape) == 2


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    h, w = 500, 200
    image = np.random.rand(h, w)

    pixel_samples = PixelSampling(image)
    coords = pixel_samples.coordinates()

    plt.imshow(image)
    plt.scatter(coords[:, 0], coords[:, 1])

    plt.show()



