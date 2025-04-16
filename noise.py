import tensorflow as tf
import cv2 as cv
import numpy as np
from skimage.util import random_noise
from skimage.transform import SimilarityTransform, warp
import math




mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()


first_image = x_train[0]


tform = SimilarityTransform(scale=1, rotation=math.radians(30), translation=(5, 1))


cv.imshow("wow",first_image)
cv.waitKey(0)

first_image = warp(first_image, tform)
first_image = random_noise(first_image, mode='gaussian', mean=0, var=0.3)

cv.imshow("wow",first_image)
cv.waitKey(0)