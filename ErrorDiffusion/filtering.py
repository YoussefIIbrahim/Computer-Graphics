from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
from PIL import Image

from ErrorDiffusion import palette

_DIFFUSION_MAPS = {
    'floyd-steinberg': (
        (1, 0, 7 / 16),
        (-1, 1, 3 / 16),
        (0, 1, 5 / 16),
        (1, 1, 1 / 16)
    ),
    'atkinson': (
        (1, 0, 1 / 8),
        (2, 0, 1 / 8),
        (-1, 1, 1 / 8),
        (0, 1, 1 / 8),
        (1, 1, 1 / 8),
        (0, 2, 1 / 8),
    ),
    'stucki': (
        (1, 0, 8 / 42),
        (2, 0, 4 / 42),
        (-2, 1, 2 / 42),
        (-1, 1, 4 / 42),
        (0, 1, 8 / 42),
        (1, 1, 4 / 42),
        (2, 1, 2 / 42),
        (-2, 2, 1 / 42),
        (-1, 2, 2 / 42),
        (0, 2, 4 / 42),
        (1, 2, 2 / 42),
        (2, 2, 1 / 42),
    ),
    'burkes': (
        (1, 0, 8 / 32),
        (2, 0, 4 / 32),
        (-2, 1, 2 / 32),
        (-1, 1, 4 / 32),
        (0, 1, 8 / 32),
        (1, 1, 4 / 32),
        (2, 1, 2 / 32),
    ),
    'sierra3': (
        (1, 0, 5 / 32),
        (2, 0, 3 / 32),
        (-2, 1, 2 / 32),
        (-1, 1, 4 / 32),
        (0, 1, 5 / 32),
        (1, 1, 4 / 32),
        (2, 1, 2 / 32),
        (-1, 2, 2 / 32),
        (0, 2, 3 / 32),
        (1, 2, 2 / 32),
    )
}


def error_diffusion_dithering(image, method='floyd-steinberg',
                              order=8):
    ni = np.array(image, 'float')

    diff_map = _DIFFUSION_MAPS.get(method.lower())

    for y in range(ni.shape[0]):
        for x in range(ni.shape[1]):
            old_pixel = ni[y, x]
            old_pixel[old_pixel < 0.0] = 0.0
            old_pixel[old_pixel > 255.0] = 255.0
            new_pixel = palette.pixel_closest_colour(old_pixel, order)
            quantization_error = old_pixel - new_pixel
            ni[y, x] = new_pixel
            for dx, dy, diffusion_coefficient in diff_map:
                xn, yn = x + dx, y + dy
                if (0 <= xn < ni.shape[1]) and (0 <= yn < ni.shape[0]):
                    ni[yn, xn] += quantization_error * diffusion_coefficient
    return palette.create_PIL_png_from_rgb_array(np.array(ni, 'uint8'))


img = Image.open('/Users/youssefiibrahim/PycharmProjects/Computer-Graphics/Filters/eye.jpg')
palette = palette.Palette.create_by_median_cut(img)
(error_diffusion_dithering(img, palette)).show()
