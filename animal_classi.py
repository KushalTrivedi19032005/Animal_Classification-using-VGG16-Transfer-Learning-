# -*- coding: utf-8 -*-
"""Animal_Classi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cHOYixTxPZxayMeTnn5KLyH5VuD2cHfH
"""

!kaggle datasets download -d borhanitrash/animal-image-classification-dataset

import zipfile
zip_ref = zipfile.ZipFile('/content/animal-image-classification-dataset.zip', 'r') # Update file path if needed
zip_ref.extractall('/content')
zip_ref.close()

pip install split-folders

import splitfolders

# Input folder containing subfolders for each class
input_folder = '/content/Animals'

# Output folder where the split datasets will be saved
output_folder = '/content/Animals_split'

# Split with a ratio for train and test (80% train, 20% test)
splitfolders.ratio(input_folder, output=output_folder, seed=1337, ratio=(.8, .2), group_prefix=None)

train_folder = '/content/Animals_split/train'
test_folder = '/content/Animals_split/val'

import tensorflow
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Flatten
from keras.applications.vgg16 import VGG16

conv_base=VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

model=Sequential()
model.add(conv_base)
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dense(3,activation='softmax'))

conv_base.trainable=False

from keras.preprocessing.image import ImageDataGenerator

batch_size=32

train_datagen=ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen=ImageDataGenerator(
    rescale=1./255
)

train_generator=train_datagen.flow_from_directory (
    train_folder,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical'
)

test_generator=test_datagen.flow_from_directory(
    test_folder,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical'
)

# train_ds = keras.utils.image_dataset_from_directory(
#     directory = '/content/train',
#     labels='inferred',
#     label_mode = 'int',
#     batch_size=32,
#     image_size=(150,150)
# )

# validation_ds = keras.utils.image_dataset_from_directory(
#     directory = '/content/test',
#     labels='inferred',
#     label_mode = 'int',
#     batch_size=32,
#     image_size=(150,150)
# )




# def process(image,label):
#     image = tensorflow.cast(image/255. ,tensorflow.float32)
#     return image,label

# train_ds = train_ds.map(process)
# validation_ds = validation_ds.map(process)



# conv_base.trainable = True

# set_trainable = False

# for layer in conv_base.layers:
#   if layer.name == 'block5_conv1':
#     set_trainable = True
#   if set_trainable:
#     layer.trainable = True
#   else:
#     layer.trainable = False

# for layer in conv_base.layers:
#   print(layer.name,layer.trainable)

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

history=model.fit(
    train_generator,
    epochs=5,
    validation_data=test_generator,
    verbose=1
)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],label='train', color='red',)
plt.plot(history.history['val_accuracy'],label='val', color='blue', )
plt.legend()
plt.show()

plt.plot(history.history['loss'],label='train', color='red', )
plt.plot(history.history['val_loss'],label='val', color='blue',)
plt.legend()
plt.show()