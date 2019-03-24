import numpy as np
from PIL import Image


class Filter:
    def __init__(self, matrix, offset, anchor, divisor=None):
        self.matrix = np.expand_dims(matrix, axis=2)
        self.shape = matrix.shape
        self.offset = offset
        self.anchor = anchor
        self.d = divisor
        if self.d is None:
            self.d = np.sum(matrix)
        if self.d == 0:
            self.d = 1


DEFAULT_BRIGHTNESS = 25
DEFAULT_CONTRAST = 2
DEFAULT_GAMMA = 2

DEFAULT_BLUR = Filter(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]), 0, (1, 1))
DEFAULT_GAUSSIAN = Filter(np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]), 0, (1, 1))
DEFAULT_SHARPEN = Filter(np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]), 0, (1, 1))
DEFAULT_EDGE = Filter(np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 0]]), 0, (1, 1))
DEFAULT_EMBOSS = Filter(np.array([[-1, -1, 0], [-1, 1, 1], [0, 1, 1]]), 0, (1, 1))


def functional_filter(image, function):
    arr = np.array(image, dtype=np.single)
    arr = function(arr)
    return Image.fromarray(np.array(arr, dtype=np.uint8))


def inversion(image):
    return functional_filter(image, lambda x: 255 - x)


def brightness_correction(image):
    return functional_filter(image, lambda x: np.clip(x + DEFAULT_BRIGHTNESS, 0, 255))


def contrast_enhancement(image):
    return functional_filter(image, lambda x: np.clip(DEFAULT_CONTRAST * (x - 64), 0, 255))


def gamma_correction(image, gamma_factor):
    return functional_filter(image, lambda x: (x / 255) ** float(gamma_factor) * 255)


def convolution_filter(image, filter):
    arr = np.array(image)
    padded = np.zeros(
        [sum(x) for x in zip(arr.shape, (filter.shape[0], filter.shape[1], 0), (filter.shape[0], filter.shape[1], 0))])
    padded[filter.shape[0]:-filter.shape[0], filter.shape[1]:-filter.shape[1], :] = arr
    padded[:filter.shape[0], :, :] = padded[filter.shape[0], :, :]
    padded[-filter.shape[0]:, :, :] = padded[-filter.shape[0], :, :]
    for i in range(filter.shape[1]):
        padded[:, i, :] = padded[:, filter.shape[1], :]
        padded[:, -i, :] = padded[:, -filter.shape[1], :]

    output = np.zeros(arr.shape)
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            output[i, j] = filter.offset + sum(sum(filter.matrix * padded[i + filter.shape[0] - filter.anchor[0]:i + 2 *
                                                                                                                 filter.shape[
                                                                                                                     0] -
                                                                                                                 filter.anchor[
                                                                                                                     0],
                                                                   j + filter.shape[1] - filter.anchor[1]:j + 2 *
                                                                                                          filter.shape[
                                                                                                              1] -
                                                                                                          filter.anchor[
                                                                                                              1],
                                                                   :])) / filter.d
    output = np.clip(output, 0, 255)
    return Image.fromarray(np.array(output, dtype=np.uint8))


def blur(image):
    return convolution_filter(image, DEFAULT_BLUR)


def gaussian(image):
    return convolution_filter(image, DEFAULT_GAUSSIAN)


def sharpen(image):
    return convolution_filter(image, DEFAULT_SHARPEN)


def edge(image):
    return convolution_filter(image, DEFAULT_EDGE)


def emboss(image):
    return convolution_filter(image, DEFAULT_EMBOSS)
