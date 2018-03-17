"""
TODO : Takes a list of path of segmented images and returns 
predicted list using model stored in utilities/keras_model/models_generated
"""

from keras.models import load_model
import cv2
import os 
import numpy as np

from keras import backend as K
from keras.models import Sequential
from keras.layers import Input, Dropout, Flatten, Conv2D, MaxPooling2D, Dense, Activation
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from keras import backend as K
import pickle
optimizer = RMSprop(lr=1e-3)
objective = 'categorical_crossentropy'

def mathsymbol():
    model = Sequential()
    model.add(Conv2D(32, (5, 5), input_shape=(45, 45, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(28, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def predict_image(path):
    K.clear_session()
    model = mathsymbol()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model.load_weights(os.path.join(dir_path,'weights.h5'))
    img = cv2.imread(path)
    # cv2.resize(img,(150,150))
    img = cv2.resize(img, (45, 45))
    image_final = np.zeros((1,45,45,3))
    # cv2.imshow('')
    image_final[0,:,:,:] = img   
    for i in image_final:
        i /= 255.0

    prediction = model.predict(image_final)
    # image_final.show
    file = open(os.path.join(dir_path,'mapping.txt'),'rb')
    L = pickle.load(file)
    ans = L[np.argmax(prediction)]
    print(ans)
    return ans
