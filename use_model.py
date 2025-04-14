import tensorflow as tf
import cv2 as cv
import numpy as np
import imutils

mnist = tf.keras.datasets.mnist

model = tf.keras.models.load_model('numberreader.h5')

def predict_number(img_path):
    img = cv.imread(img_path)
    img = imutils.resize(img, width=28)
    
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

# img = np.invert(np.array([img]))
# predict_number("screenshot.png")
