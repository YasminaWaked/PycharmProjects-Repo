import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import tensorflow

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

classes = 43
image_size = (30, 30)
def build_model():
    data = []
    labels = []
    cur_path = os.getcwd()  #current working directory

    for i in range(classes):
        path = os.path.join(cur_path, 'Train', str(i))
        images = os.listdir(path)
        for a in images:
            try:
                image = Image.open(os.path.join(path, a))
                image = image.resize(image_size)
                image = np.array(image)
                data.append(image)
                labels.append(i)
                print(i, "appended")
            except:
                print("Error loading image")

    data = np.array(data)
    labels = np.array(labels)

    print('Data shape: ', data.shape)
    print("Labels shape: ", labels.shape)

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    y_train = to_categorical(y_train, classes)
    y_test = to_categorical(y_test, classes)

    print('X_train shape: ', X_train.shape)
    print('X_test shape: ', X_test.shape)
    print('y_train shape: ', y_train.shape)
    print('y_test shape: ', y_test.shape)

    #build model
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=X_train.shape[1:]))
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(classes, activation='softmax'))

    #compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    #train and validate model
    batch_size = 32
    epochs = 15
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, y_test))

    #plotting graphs for accuracy
    plt.figure(0)
    plt.plot(history.history['accuracy'], label='training accuracy')
    plt.plot(history.history['val_accuracy'], label='val accuracy')
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    plt.figure(1)
    plt.plot(history.history['loss'], label='training loss')
    plt.plot(history.history['val_loss'], label='val loss')
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    #save model
    model.save('traffic_sign_model.h5')

    #testinf accuracy on dataset
    test_data = pd.read_csv('Test.csv')
    test_labels = test_data['ClassId'].values
    test_imgs = test_data['Path'].values

    test_data = []

    for img in test_imgs:
        image = Image.open(img)
        image = image.resize(image_size)
        test_data.append(np.array(image))

    X_test = np.array(test_data)

    #predict classes
    pred = model.predict(X_test)
    pred = np.argmax(pred, axis=1)

    #accuracy with the test data
    test_accuracy = accuracy_score(test_labels, pred)
    print("Test Accuracy: ", test_accuracy)

def classify_image(file_path):
    #load model
    model = load_model('traffic_sign_model.h5')

    #dictionary too label all traffic sign classes
    classes = {
        1: 'Speed limit (20km/h)',
        2: 'Speed limit (30km/h)',
        3: 'Speed limit (50km/h)',
        4: 'Speed limit (60km/h)',
        5: 'Speed limit (70km/h)',
        6: 'Speed limit (80km/h)',
        7: 'End of Speed limit (80km/h)',
        8: 'Speed limit (100km/h)',
        9: 'Speed limit (120km/h)',
        10: 'No passing',
        11: 'No passing veh over 3.5 tons',
        12: 'Right-of-way at intersection',
        13: 'Priority road',
        14: 'Yield',
        15: 'Stop',
        16: 'No vehicles',
        17: 'Veh > 3.5 tons prohibited',
        18: 'No entry',
        19: 'General caution',
        20: 'Dangerous curve left',
        21: 'Dangerous curve right',
        22: 'Double curve',
        23: 'Bumpy road',
        24: 'Slippery road',
        25: 'Road narrows on the right',
        26: 'Road work',
        27: 'Traffic signals',
        28: 'Pedestrians',
        29: 'Children crossing',
        30: 'Bicycles crossing',
        31: 'Beware of ice/snow',
        32: 'Wild animals crossing',
        33: 'End speed + passing limits',
        34: 'Turn right ahead',
        35: 'Turn left ahead',
        36: 'Ahead only',
        37: 'Go straight or right',
        38: 'Go straight or left',
        39: 'Keep right',
        40: 'Keep left',
        41: 'Roundabout mandatory',
        42: 'End of no passing',
        43: 'End of no passing veh > 3.5 tons'
    }

    image = Image.open(file_path)
    image = image.resize((30, 30))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    pred = model.predict([image])[0]
    pred = np.argmax(pred)
    sign = classes[pred + 1]
    print(pred+1)
    print(sign)

if __name__ == '__main__':
    file_path = 'speed_limit_70.jpeg'
    #build_model()
    classify_image(file_path)
