from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dropout, Concatenate, Input, UpSampling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import plot_model
from tensorflow.keras.initializers import he_normal, he_uniform
from tensorflow.keras.activations import softmax, relu
from tensorflow.keras.regularizers import l1, l2, l1_l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy, Precision, Recall 
from DICE import *
import numpy as np
import matplotlib.pyplot as plt

'''
This file contains implementation of UNet architecture
'''


def get_UNET(input_shape, classes = 3):
  inputs = Input(input_shape)
  conv1 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(inputs)
  conv1 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv1)
  drop1 = Dropout(0.5)(conv1)
  max_pool1 = MaxPool2D(pool_size=(2, 2))(drop1)

  conv2 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool1)
  conv2 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv2)
  drop2 = Dropout(0.5)(conv2)
  max_pool2 = MaxPool2D(pool_size=(2, 2))(drop2)

  conv3 = Conv2D(filters=256, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool2)
  conv3 = Conv2D(filters=256, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv3)
  drop3 = Dropout(0.5)(conv3)
  max_pool3 = MaxPool2D(pool_size=(2, 2))(drop3)

  conv4 = Conv2D(filters=512, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool3)
  conv4 = Conv2D(filters=512, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv4)
  drop4 = Dropout(0.5)(conv4)
  max_pool4 = MaxPool2D(pool_size=(2, 2))(conv4)

  conv5 = Conv2D(filters=1024, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool4)
  conv5 = Conv2D(filters=1024, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv5)
  drop5 = Dropout(0.5)(conv5)

  #print("merge1")
  up_conv6 = Conv2D(filters=512, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(drop5))
  merge6 = Concatenate(axis=3)([drop4, up_conv6])
  conv7 = Conv2D(filters=512, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge6)
  conv7 = Conv2D(filters=512, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv7)
  
  #print("merge2")
  up_conv8 = Conv2D(filters=256, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(conv7))
  merge8 = Concatenate(axis=3)([conv3, up_conv8])
  conv9 = Conv2D(filters=256, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge8)
  conv9 = Conv2D(filters=256, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv9)

  #print("merge3")
  up_conv10 = Conv2D(filters=128, kernel_size=(2, 2), activation = None, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(conv9))
  merge10 = Concatenate(axis=3)([conv2, up_conv10])
  conv11 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge10)
  conv11 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv11)

  #print("merge4")
  up_conv12 = Conv2D(filters=64, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(conv11))
  merge12 = Concatenate(axis=3)([conv1, up_conv12])
  conv13 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge12)
  conv13 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv13)

  conv14 = Conv2D(filters=2, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal')(conv13)
  conv15 = Conv2D(filters=classes, kernel_size=(1, 1), activation = softmax)(conv14)

  
  model = Model(inputs = inputs, outputs = conv15)


  return model




def get_small_UNET(input_shape, classes):
    
  inputs = Input(input_shape)

  conv1 = Conv2D(filters=16, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(inputs)
  drop1 = Dropout(0.1)(conv1)
  conv1 = Conv2D(filters=16, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop1)
  max_pool1 = MaxPool2D(pool_size=(2, 2))(conv1)

  conv2 = Conv2D(filters=32, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool1)
  drop2 = Dropout(0.1)(conv2)
  conv2 = Conv2D(filters=32, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop2)
  max_pool2 = MaxPool2D(pool_size=(2, 2))(conv2)

  conv3 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool2)
  drop3 = Dropout(0.2)(conv3)
  conv3 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop3)
  max_pool3 = MaxPool2D(pool_size=(2, 2))(conv3)

  conv4 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool3)
  drop4 = Dropout(0.2)(conv4)
  conv4 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop4)
  max_pool4 = MaxPool2D(pool_size=(2, 2))(conv4)

  conv5 = Conv2D(filters=256, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(max_pool4)
  conv5 = Conv2D(filters=256, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(conv5)
  drop5 = Dropout(0.3)(conv5)

  # UP

  up_conv6 = Conv2D(filters=128, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(drop5))
  merge6 = Concatenate(axis=3)([up_conv6, conv4])
  conv6 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge6)
  drop6 = Dropout(0.2)(conv6)
  conv6 = Conv2D(filters=128, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop6)

  up_conv7 = Conv2D(filters=64, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(conv6))
  merge7 = Concatenate(axis=3)([up_conv7, conv3])
  conv7 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge7)
  drop7 = Dropout(0.2)(conv7)
  conv7 = Conv2D(filters=64, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop7)

  up_conv8 = Conv2D(filters=32, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(conv7))
  merge8 = Concatenate(axis=3)([up_conv8, conv2])
  conv8 = Conv2D(filters=32, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge8)
  drop8 = Dropout(0.1)(conv8)
  conv8 = Conv2D(filters=32, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop8)

  up_conv9 = Conv2D(filters=16, kernel_size=(2, 2), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(UpSampling2D(size=(2, 2))(conv8))
  merge9 = Concatenate(axis=3)([up_conv9, conv1])
  conv9 = Conv2D(filters=16, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(merge9)
  drop9 = Dropout(0.1)(conv9)
  conv9 = Conv2D(filters=16, kernel_size=(3, 3), activation = relu, padding = 'same', kernel_initializer='he_normal', kernel_regularizer=None)(drop9)

  outputs = Conv2D(filters=classes, kernel_size=(1, 1), activation='sigmoid')(conv9)

  model = Model(inputs=inputs, outputs=outputs)

  return model




#model = get_UNET((512,512, 1))
