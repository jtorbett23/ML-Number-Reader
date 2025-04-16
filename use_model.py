import tensorflow as tf
import cv2 as cv
import numpy as np
import imutils
from skimage import io
from skimage.transform import resize, SimilarityTransform, warp
import math

mnist = tf.keras.datasets.mnist

model = tf.keras.models.load_model('numberreader.h5')


def prepare_image_cv(img_path):
    img = cv.imread(img_path)
    img = imutils.resize(img, width=28)
    return img

def prepare_image_sk(img_path):
    img = io.imread(img_path)
    img = resize(img, (28,28),anti_aliasing=True)
    return img

def predict_number_with_path(img_path):

    img = prepare_image_sk(img_path)
    # get (i, j) positions of all RGB pixels that are black (i.e. [0, 0, 0])
    non_black_pixels = np.where(
        (img[:, :, 0] != 0) & 
        (img[:, :, 1] != 0) & 
        (img[:, :, 2] != 0)
    )

    # set all non black pixels to white
    img[non_black_pixels] = [255, 255, 255]

    cv.imwrite("resize.png",img)
    img = img[:,:,0]
    img = np.array([img])
    
    predicition = model.predict(img)
    print(predicition)
    print(f"The digit is probably {np.argmax(predicition)}")

def predict_number(img):
    img = np.flipud(img)
    img = np.rot90(img, -1)
    img = resize(img, (28,28),anti_aliasing=True)
    # get (i, j) positions of all RGB pixels that are black (i.e. [0, 0, 0])

    non_black_pixels = np.where(
        (img[:, :, 0] != 0) & 
        (img[:, :, 1] != 0) & 
        (img[:, :, 2] != 0)
    )

    # set all non black pixels to white
    img[non_black_pixels] = [255, 255, 255]

    cv.imwrite("resize.png",img)
    img = img[:,:,0]
    img = np.array([img])
    
    predicition = model.predict(img)
    print(predicition)
    print(f"The digit is probably {np.argmax(predicition)}")
