import cv2
import numpy as np
import math
import copy
from matplotlib import pyplot as plt


def inversion(image):
    for x in range(len(image)):
        for y in range(len(image[x])):
            image[x][y][0] = 255 - image[x][y][0]
            image[x][y][1] = 255 - image[x][y][1]
            image[x][y][2] = 255 - image[x][y][2]
    return image


def truncate(value):

    if value < 0:
        value = 0

    if value > 255:
        value = 255

    return value


def brightness(image, const):
    for x in range(len(image)):
        for y in range(len(image[x])):
            image[x][y][0] = truncate(image[x][y][0] + const)
            image[x][y][1] = truncate(image[x][y][1] + const)
            image[x][y][2] = truncate(image[x][y][2] + const)
    return image


def contrast(image, const):
    new_image = np.zeros((len(image), len(image[0]), 3), dtype=np.uint8)
    fact = (259 * (const + 255)) / (255 * (259 - const))
    print(fact)
    for x in range(len(image)):
        for y in range(len(image[x])):
            new_image[x][y][0] = truncate((fact * (image[x][y][0] - 128)) + 128)
            new_image[x][y][1] = truncate((fact * (image[x][y][1] - 128)) + 128)
            new_image[x][y][2] = truncate((fact * (image[x][y][2] - 128)) + 128)
    return new_image


def gaussianfilter(image):
    new_image = np.zeros((len(image), len(image[0])), dtype=np.uint8)
    filtering = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    for x in range(len(image)):
        for y in range(len(image[x])):

            if x-1 < 0:

                left = image[x + 1][y]
                right = image[x + 1][y]

                if y-1 < 0:
                    left_down = image[x+1][y+1]
                    right_up = image[x+1][y+1]
                    up = image[x][y+1]
                    down = image[x][y+1]
                    right_down = image[x+1][y+1]
                    left_up = image[x+1][y+1]

                elif y+1 == len(image[x]):
                    left_up = image[x+1][y-1]
                    right_down = image[x+1][y-1]
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_down = image[x+1][y-1]
                    right_up = image[x+1][y-1]

                else:
                    left_up = image[x+1][y+1]
                    left_down = image[x+1][y-1]
                    up = image[x][y-1]
                    down = image[x][y+1]
                    right_up = image[x+1][y-1]
                    right_down = image[x+1][y+1]

            elif x+1 == len(image):

                right = image[x-1][y]
                left = image[x-1][y]

                if y-1 < 0:
                    right_down = image[x-1][y+1]
                    left_up = image[x-1][y+1]
                    up = image[x][y+1]
                    down = image[x][y+1]
                    right_up = image[x-1][y+1]
                    left_down = image[x-1][y+1]

                elif y+1 == len(image[x]):
                    left_down = image[x-1][y-1]
                    right_up = image[x-1][y-1]
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_up = image[x-1][y-1]
                    right_down = image[x-1][y-1]

                else:
                    up = image[x][y - 1]
                    down = image[x][y + 1]
                    left_up = image[x-1][y-1]
                    left_down = image[x-1][y+1]
                    right_up = image[x-1][y+1]
                    right_down = image[x-1][y-1]

            else:
                left = image[x - 1][y]
                right = image[x+1][y]

                if y-1 < 0:
                    up = image[x][y+1]
                    down = image[x][y+1]
                    left_up = image[x+1][y+1] # =right_down
                    right_up = image[x-1][y+1] # =left_down
                    left_down = image[x-1][y+1]
                    right_down = image[x+1][y+1]

                elif y+1 == len(image[x]):
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_down = image[x+1][y-1] # =right_up
                    right_down = image[x-1][y-1] # =left_up
                    left_up = image[x-1][y-1]
                    right_up = image[x+1][y-1]
                else:
                    up = image[x][y-1]
                    down = image[x][y+1]
                    left_up = image[x-1][y-1]
                    left_down = image[x-1][y+1]
                    right_up = image[x+1][y-1]
                    right_down = image[x+1][y+1]

            elems = np.array([[left_up, up, right_up], [left, image[x][y], right], [left_down, down, right_down]])
            new_image[x][y] = (sum(sum(filtering * elems))/16)
    return new_image


def sharpeningfilter(image):
    new_image = np.zeros((len(image), len(image[0])), dtype=np.uint8)
    filtering = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    for x in range(len(image)):
        for y in range(len(image[x])):

            if x-1 < 0:

                left = image[x + 1][y]
                right = image[x + 1][y]

                if y-1 < 0:
                    left_down = image[x+1][y+1]
                    right_up = image[x+1][y+1]
                    up = image[x][y+1]
                    down = image[x][y+1]
                    right_down = image[x+1][y+1]
                    left_up = image[x+1][y+1]

                elif y+1 == len(image[x]):
                    left_up = image[x+1][y-1]
                    right_down = image[x+1][y-1]
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_down = image[x+1][y-1]
                    right_up = image[x+1][y-1]

                else:
                    left_up = image[x+1][y+1]
                    left_down = image[x+1][y-1]
                    up = image[x][y-1]
                    down = image[x][y+1]
                    right_up = image[x+1][y-1]
                    right_down = image[x+1][y+1]

            elif x+1 == len(image):

                right = image[x-1][y]
                left = image[x-1][y]

                if y-1 < 0:
                    right_down = image[x-1][y+1]
                    left_up = image[x-1][y+1]
                    up = image[x][y+1]
                    down = image[x][y+1]
                    right_up = image[x-1][y+1]
                    left_down = image[x-1][y+1]

                elif y+1 == len(image[x]):
                    left_down = image[x-1][y-1]
                    right_up = image[x-1][y-1]
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_up = image[x-1][y-1]
                    right_down = image[x-1][y-1]

                else:
                    up = image[x][y - 1]
                    down = image[x][y + 1]
                    left_up = image[x-1][y-1]
                    left_down = image[x-1][y+1]
                    right_up = image[x-1][y+1]
                    right_down = image[x-1][y-1]

            else:
                left = image[x - 1][y]
                right = image[x+1][y]

                if y-1 < 0:
                    up = image[x][y+1]
                    down = image[x][y+1]
                    left_up = image[x+1][y+1] # =right_down
                    right_up = image[x-1][y+1] # =left_down
                    left_down = image[x-1][y+1]
                    right_down = image[x+1][y+1]

                elif y+1 == len(image[x]):
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_down = image[x+1][y-1] # =right_up
                    right_down = image[x-1][y-1] # =left_up
                    left_up = image[x-1][y-1]
                    right_up = image[x+1][y-1]
                else:
                    up = image[x][y-1]
                    down = image[x][y+1]
                    left_up = image[x-1][y-1]
                    left_down = image[x-1][y+1]
                    right_up = image[x+1][y-1]
                    right_down = image[x+1][y+1]

            elems = np.array([[left_up, up, right_up], [left, image[x][y], right], [left_down, down, right_down]])
            new_image[x][y] = image[x][y] + (sum(sum(filtering * elems))/16)
    return new_image


def sobelfilter(image):

    gx_filtering = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gy_filtering = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    blank_image = np.zeros((len(image), len(image[0])), dtype=np.uint8)

    for x in range(len(image)):
        for y in range(len(image[x])):

            if x-1 < 0:

                left = image[x + 1][y]
                right = image[x + 1][y]

                if y-1 < 0:
                    left_down = image[x+1][y+1]
                    right_up = image[x+1][y+1]
                    up = image[x][y+1]
                    down = image[x][y+1]
                    right_down = image[x+1][y+1]
                    left_up = image[x+1][y+1]

                elif y+1 == len(image[x]):
                    left_up = image[x+1][y-1]
                    right_down = image[x+1][y-1]
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_down = image[x+1][y-1]
                    right_up = image[x+1][y-1]

                else:
                    left_up = image[x+1][y+1]
                    left_down = image[x+1][y-1]
                    up = image[x][y-1]
                    down = image[x][y+1]
                    right_up = image[x+1][y-1]
                    right_down = image[x+1][y+1]

            elif x+1 == len(image):

                right = image[x-1][y]
                left = image[x-1][y]

                if y-1 < 0:
                    right_down = image[x-1][y+1]
                    left_up = image[x-1][y+1]
                    up = image[x][y+1]
                    down = image[x][y+1]
                    right_up = image[x-1][y+1]
                    left_down = image[x-1][y+1]

                elif y+1 == len(image[x]):
                    left_down = image[x-1][y-1]
                    right_up = image[x-1][y-1]
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_up = image[x-1][y-1]
                    right_down = image[x-1][y-1]

                else:
                    up = image[x][y - 1]
                    down = image[x][y + 1]
                    left_up = image[x-1][y-1]
                    left_down = image[x-1][y+1]
                    right_up = image[x-1][y+1]
                    right_down = image[x-1][y-1]

            else:
                left = image[x - 1][y]
                right = image[x+1][y]

                if y-1 < 0:
                    up = image[x][y+1]
                    down = image[x][y+1]
                    left_up = image[x+1][y+1] # =right_down
                    right_up = image[x-1][y+1] # =left_down
                    left_down = image[x-1][y+1]
                    right_down = image[x+1][y+1]

                elif y+1 == len(image[x]):
                    down = image[x][y-1]
                    up = image[x][y-1]
                    left_down = image[x+1][y-1] # =right_up
                    right_down = image[x-1][y-1] # =left_up
                    left_up = image[x-1][y-1]
                    right_up = image[x+1][y-1]
                else:
                    up = image[x][y-1]
                    down = image[x][y+1]
                    left_up = image[x-1][y-1]
                    left_down = image[x-1][y+1]
                    right_up = image[x+1][y-1]
                    right_down = image[x+1][y+1]

            elems = np.array([[left_up, up, right_up], [left, image[x][y], right], [left_down, down, right_down]])
            blank_image[x][y] = math.sqrt(
                int(np.sum(elems * gx_filtering)) ** 2 + int(np.sum(elems * gy_filtering)) ** 2)

    return blank_image


def robertscrossfilter(image):
    gx_filtering = np.array([[1, 0], [0, -1]])
    gy_filtering = np.array([[0, 1], [-1, 0]])
    new_image = np.zeros((len(image), len(image[0])), dtype=np.uint8)
    for x in range(len(image)):
        for y in range(len(image[x])):

            if x + 1 == len(image):

                right = image[x - 1][y]

                if y - 1 < 0:
                    right_down = image[x][y]
                    down = image[x][y + 1]

                elif y + 1 == len(image[x]):
                    down = image[x][y - 1]
                    right_down = image[x - 1][y - 1]

                else:
                    down = image[x][y + 1]
                    right_down = image[x - 1][y - 1]

            else:

                right = image[x + 1][y]

                if y + 1 == len(image[x]):

                    down = image[x][y-1]

                    if x + 1 == len(image):
                        right_down = image[x][y]

                    else:
                        right_down = image[x-1][y-1]

                else:
                    down = image[x][y + 1]
                    right_down = image[x + 1][y + 1]

            elems = np.array([[image[x][y], right], [down, right_down]])

            gx = (sum(sum(gx_filtering * elems)))
            gy = (sum(sum(gy_filtering * elems)))
            new_image[x][y] = math.sqrt(gx ** 2 + gy ** 2)

    return new_image