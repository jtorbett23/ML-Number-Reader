import tensorflow as tf
import cv2 as cv
import numpy as np
from skimage.util import random_noise
from skimage.transform import SimilarityTransform, warp, resize
import math
import random

MAX_NOISE = 0.1
MIN_NOISE = 0.05
MAX_ROT = 20
MAX_OFFSET = 5
MIN_SCALE = 0.8
MAX_SCALE = 1.1

def get_random_float(min, max):
    return random.uniform(min, max)

def get_random_int(min, max):
    return random.randint(min, max)

def apply_noise(images):
    print("Applying noise...")
    noisy_images = []
    for image in images:
        noise = get_random_float(MIN_NOISE, MAX_NOISE)
        offset_x = get_random_int(-MAX_OFFSET, MAX_OFFSET)
        offset_y = get_random_int(-MAX_OFFSET, MAX_OFFSET)
        rotation_degs = get_random_float(-MAX_ROT, MAX_ROT)
        rotation_rads = math.radians(rotation_degs)
        scale = get_random_float(MIN_SCALE, MAX_SCALE)

        # print(noise)
        # print(offset_x)
        # print(offset_y)
        # print(rotation_degs)
        # print(scale)

        tform = SimilarityTransform(scale=scale, rotation=math.radians(rotation_rads), translation=(offset_x, offset_y))
        image = warp(image, tform)
        image = random_noise(image, mode='gaussian', mean=0, var=noise)
        noisy_images.append(image)
    
    print("Noise applied")
    return noisy_images

def test():
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()


    first_image = x_train[0]
    noisy_images = apply_noise([first_image])
    # noisy_images_first = noisy_images[0] * 255

    # cv.imwrite("images/mnist-noisy-2.png", noisy_images_first)

    cv.imshow("wow",resize(first_image, (360,360)))
    cv.waitKey(0)

    cv.imshow("wow",resize(noisy_images[0], (360,360)))
    cv.waitKey(0)

# test()