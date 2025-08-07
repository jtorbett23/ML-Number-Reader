import tensorflow as tf
# import cv2 as cv
import numpy as np
# import imutils
from skimage import io
from skimage.transform import resize

# model = tf.keras.models.load_model('numberreader.h5')


# def prepare_image_cv(img_path):
#     img = cv.imread(img_path)
#     # cv.imwrite("images/original.png",img)
#     img = imutils.resize(img, width=28)
#     return img

def prepare_image_sk(img_path):
    img = io.imread(img_path)
    # cv.imwrite("images/original.png",img)
    img = resize(img, (28,28),anti_aliasing=True)
    return img

# def predict_number_with_path(img_path):
#     img = prepare_image_sk(img_path)
    
#     non_black_pixels = np.where(
#         (img[:, :, 0] > (15/255)) 
#     )

#     # set all non black pixels to white
#     human_image = img
#     human_image[non_black_pixels] = (human_image[non_black_pixels] * 255) + 75

#     img[non_black_pixels] = img[non_black_pixels] + (75/255)

#     # cv.imwrite("images/resize.png",img)
#     img = img[:,:,0]
#     img = np.array([img])
    
#     predicition = model.predict(img)
#     print(predicition)
#     print(f"The digit is probably {np.argmax(predicition)}")

def predict_number(img):
    model = tf.keras.models.load_model('numberreader.h5')
    img = np.flipud(img)
    img = np.rot90(img, -1)
    non_white_pixels = np.where(
        (img[:, :, 0] < 230) 
    )
    img[non_white_pixels] = 0
    # cv.imwrite("images/original.png",img)

    # if i need to use just numpy try - img = img[::12, ::12]

    img = resize(img, (28,28),anti_aliasing=True)
    
    # get (i, j) positions of all RGB pixels that are black (i.e. [0, 0, 0])

    non_black_pixels = np.where(
        (img[:, :, 0] > (15/255)) 
    )

    # set all non black pixels to white
    human_image = img
    human_image[non_black_pixels] = (human_image[non_black_pixels] * 255) + 75

    img[non_black_pixels] = img[non_black_pixels] + (75/255)

    # cv.imwrite("images/resize.png",human_image)
    img = img[:,:,0]
    img = np.array([img])
    
    predicition = model.predict(img)
    number : int = np.argmax(predicition)
    return number