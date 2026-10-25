import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten

cur_path = os.getcwd()
train_dir = os.path.join(cur_path, 'data', 'train')
validation_dir = os.path.join(cur_path, 'data', 'test')

train_datagen = ImageDataGenerator(
    rescale = 1. / 255,
    rotation_range = 20,
    horizontal_flip = True,
    shear_range = 0.2,
    fill_mode = 'nearest'
)

test_datagen = ImageDataGenerator(
    rescale = 1. / 255,
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (150, 150),
    batch_size=4,
    class_mode='sparse'
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=4,
    class_mode='sparse'
)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPool2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPool2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPool2D(2, 2),
    Conv2D(512, (3, 3), activation='relu'),
    MaxPool2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(7, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch=25,
    epochs=15,
    validation_data=validation_generator, #provides data to evaluate model's performance during training
    validation_steps=5, #number of batches to consider as one validation epoch
    verbose=2 #amount of information printed during training. Prints one line per epoch to show progress
)

plt.figure(0)
plt.plot(history.history['accuracy'], label='training accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()

plt.figure(0)
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

model.save('hand_gesture_model.h5')
