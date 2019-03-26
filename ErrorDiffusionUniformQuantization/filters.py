import numpy as np
from PIL import Image

DIFFUSION_MAPS = {
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
    'stucky': (
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
    'sierra': (
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


def grayscale(im):
    image = np.array(im)
    new_image = np.zeros((len(image), len(image[0])), dtype=np.uint8)
    for i in range(len(image)):
        for j in range(len(image[i])):
            red = image[i][j][0]
            green = image[i][j][1]
            blue = image[i][j][2]
            new_image[i][j] = red * 0.3 + green * 0.59 + blue * 0.11

    return Image.fromarray((np.array(new_image, 'uint8')))


def useFilter(im, m, method='floyd-steinberg', t=0.5):
    image = grayscale(im)
    diff_map = DIFFUSION_MAPS.get(method.lower())
    ni = np.array(image, 'float')
    b = np.zeros((len(ni), len(ni[0])), dtype=np.uint8)
    diff = 255 / (m - 1)

    for y in range(ni.shape[0]):
        for x in range(ni.shape[1]):

            c = ni[y][x]
            b[y][x] = int(np.floor((c + t * diff) / diff) * diff)
            qerror = ni[y][x] - b[y][x]

            ni[y, x] = b[y][x]

            for dx, dy, diffusion_coefficient in diff_map:
                xn, yn = x + dx, y + dy
                if (0 <= xn < ni.shape[1]) and (0 <= yn < ni.shape[0]):
                    ni[yn, xn] += qerror * diffusion_coefficient
    return Image.fromarray(np.array(ni, 'uint8'))
