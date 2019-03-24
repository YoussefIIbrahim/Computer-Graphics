from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
from PIL import Image


def np2pil(img):
    return Image.fromarray(np.array(img, 'uint8'))


def pil2np(img):
    return np.array(img, 'uint8')
