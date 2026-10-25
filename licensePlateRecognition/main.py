import cv2
import os
import numpy as np
import imutils
import pytesseract
import pandas as pd
import time
import re

images_folder = 'images/'
actual_data = pd.read_csv('actual_data.csv', sep = ";")

data_to_append = []

def process_image(image_path):
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=500)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            numberPlateCnt = approx
            break

    mask = np.zeros(gray_image.shape, np.uint8)
    mask = cv2.drawContours(mask, [numberPlateCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(image, image, mask=mask)

    config = ('-l eng --oem 1 --psm 3')
    detected_plate = pytesseract.image_to_string(new_image, config=config)
    detected_plate = detected_plate.replace(' ', '').replace('\n', '')
    detected_plate = re.sub(r'[^a-zA-Z0-9]', '', detected_plate).upper()
    return detected_plate

def calculate_accuracy(detected_plate, actual_plate):
    detected_chars = list(detected_plate.lower())
    actual_chars = list(actual_plate.lower())
    corrected_chars = [d == a for d, a in zip(detected_chars, actual_chars)]
    return (sum(corrected_chars) / len(actual_chars)) * 100


for image_file in os.listdir(images_folder):
    if image_file.endswith(('png', 'jpg', 'jpeg')): #check if file is an image
        image_path = os.path.join(images_folder, image_file)
        print('Image path: ', image_path)

        #find actual number plate corresponding to image file
        actual_plate = actual_data[actual_data['image_file'] == image_file]['actual_number_plate'].values[0]
        print('Actual plate: ', actual_plate)

        detected_plate = process_image(image_path)
        print('Detected plate: ', detected_plate)

        accuracy = calculate_accuracy(detected_plate, actual_plate)
        data_to_append.append({'data': time.asctime(time.localtime(time.time())), 'actual_numer_plate': actual_plate, 'v_numeber': detected_plate, 'accuracy': accuracy})
        existing_data = pd.DataFrame(columns=['date', 'actual_numer_plate', 'v_number', 'accuracy'])
        new_data = pd.DataFrame(data_to_append)

        existing_data = existing_data.dropna(axis=1, how='all') #removes columns that have all values null
        new_data = new_data.dropna(axis=1, how='all')

        updated_data = pd.concat([existing_data, new_data], ignore_index=True) #concatinates (joins) existing data and new data to make updated data
        updated_data.to_csv('data.csv', index=False)

        print(updated_data)
