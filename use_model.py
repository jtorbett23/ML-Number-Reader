import tensorflow as tf
import numpy as np
from skimage import io
from skimage.transform import resize

def prepare_image_sk(img_path):
    img = io.imread(img_path)
    img = resize(img, (28,28),anti_aliasing=True)
    return img

def predict_number(img):
    model = tf.keras.models.load_model('numberreader.h5')
    img = np.flipud(img)
    img = np.rot90(img, -1)
    non_white_pixels = np.where(
        (img[:, :, 0] < 230) 
    )
    img[non_white_pixels] = 0


    img = resize(img, (28,28),anti_aliasing=True)
    
    # get (i, j) positions of all RGB pixels that are black (i.e. [0, 0, 0])
    non_black_pixels = np.where(
        (img[:, :, 0] > (15/255)) 
    )

    # set all non black pixels to white
    human_image = img
    human_image[non_black_pixels] = (human_image[non_black_pixels] * 255) + 75

    img[non_black_pixels] = img[non_black_pixels] + (75/255)

    img = img[:,:,0]
    img = np.array([img])
    
    predicition = model.predict(img)
    number : int = np.argmax(predicition)
    return number