"""
Quantization - Uniform gray-level
"""

import numpy as np
from PIL import Image


def quantize(image, levels, maxCount=255, displayLevels=256):
    im = np.array(image)
    returnImage = im

    if displayLevels is None:
        # by default don't re-expand the image
        displayCount = levels
    elif displayLevels > 0:
        displayCount = displayLevels - 1
    else:
        print("displayLevels is an invalid value")
        return returnImage

    if (levels > 0) and (levels < maxCount):
        levels = levels - 1
    else:
        print("levels needs to be a positive value, and smaller than the maxCount")
        return returnImage

    # uniform method from lecture
    returnImage = np.floor((im / ((maxCount + 1) / float(levels)))) * (displayCount / levels)

    return Image.fromarray(np.array(returnImage, 'uint8'))
