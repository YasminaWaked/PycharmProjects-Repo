import cv2
import tkinter as tk
from tkinter import filedialog

def apply_grayscale_filter(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def crop_image(image, x, y, width, height):
    cropped_image = image[y:y + height, x:x + width]
    return cropped_image

def show_user_input_img():
    root = tk.Tk()
    root.withdraw()

    # Ask the user to select an image file from file explorer using the file dialog
    file_object = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*.png')])

    # Check if the user selected a file
    if file_object is None:
        print("No file selected")
        return

    # Get the file path from the file object
    image_path = file_object.name

    # Read the file
    image = cv2.imread(image_path)

    # Display the image in a window
    cv2.imshow('Image', image)

    # Apply grayscale filter
    grayscale_image = apply_grayscale_filter(image)

    # Display the grayscale image in a window
    cv2.imshow("Grayscale Image", grayscale_image)

    # Wait until a key is pressed and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def rotate_image(image, angle):
    center = (image.shape[1] // 2, image.shape[0] // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
    return rotated_image


def main():
    image_path = 'sample.jpeg'
    image = cv2.imread(image_path)

    if image is None:
        print('Error: Unable to load image')
        return

    cropped_image = crop_image(image, x=100, y=100, width=200, height=200)

    cv2.imshow("Original image", image)
    cv2.imshow("Cropped image", cropped_image)

    resized_image = resize_image(image, scale_percent=50)
    cv2.imshow("Resized Image", resized_image)

    rotated_image = rotate_image(image, angle=30)
    cv2.imshow("Rotated Image", rotated_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # apply_grayscale_filter(image)
    # show_user_input_img()
    main()
