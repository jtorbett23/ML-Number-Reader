import tensorflow as tf
import cv2 as cv
import numpy as np
from skimage.util import random_noise
from skimage.transform import SimilarityTransform, warp
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

        tform = SimilarityTransform(scale=scale, rotation=math.radians(rotation_rads), translation=(offset_x, offset_y))
        image = warp(image, tform)
        image = random_noise(image, mode='gaussian', mean=0, var=noise)
        noisy_images.append(image)
    
    return noisy_images

