import cv2
import matplotlib.pyplot as plt


image_path = 'tree.png'
original_image = cv2.imread(image_path)
height, width = original_image.shape[:2]
scale = 600 / max(height, width)
image = cv2.resize(original_image, None, fx=scale, fy=scale)

def pixelFrequencyHistogram():
    histogram = cv2.calcHist([image], [0], None, [254], [0, 256])
    cv2.imshow('Original Image', image)

    plt.figure(figsize=(8, 6))
    plt.plot(histogram, color='black')
    plt.title('Image Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.xlim([0, 256])
    plt.grid()
    plt.show()

def colorFrequencyHistogram():
    red_hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    green_hist = cv2.calcHist([image], [1], None, [256], [0, 256])
    blue_hist = cv2.calcHist([image], [2], None, [256], [0, 256])

    cv2.imshow('Original Image', image)
    plt.figure(figsize=(8, 6))
    plt.subplot(3, 1, 1) #create suplot in a 3 row, 1-column grid, and it is currently 1st subplot (red histogram)
    plt.plot(red_hist, color='red')
    plt.title('Red Histogram')

    plt.subplot(3, 1, 2) #currently 2nd subplot (green histogram)
    plt.plot(green_hist, color='green')
    plt.title('Green Histogram')

    plt.subplot(3, 1, 3) #currently 3rd subplot (blue histogram)
    plt.plot(blue_hist, color='blue')
    plt.title('Blue Histogram')

    plt.tight_layout()
    plt.show()


def histogramEqualization():
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    cv2.imshow('Original Image', image)
    cv2.imshow('Gray Image', gray_image)
    cv2.imshow('Equalized Image', equalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

histogramEqualization()
