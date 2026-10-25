import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np

def flipImage():
    #load image from file
    image = cv2.imread('tree.jpg')

    #flip image horizontally
    flipped_horizontal = cv2.flip(image, 1)

    #flip image vertically
    flipped_vertical = cv2.flip(image, 0)

    #flip image horizontally and vertically (mirror)
    flipped_both = cv2.flip(image, -1)

    #display images
    cv2.imshow('Original Image', image)
    cv2.imshow('Horizontal Image', flipped_horizontal)
    cv2.imshow('Vertical Image', flipped_vertical)
    cv2.imshow('Mirrored Image', flipped_both)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

display_image = None
selected_points = []
dots = None
def scan():
    def mouse_callback(event, x, y, flags, param):
        global selected_points
        if event == cv2.EVENT_LBUTTONUP:
            if len(selected_points) < 4:
                selected_points.append((x, y))
                cv2.circle(dots, (x, y), 5, (0, 0, 255), -1)
                print(selected_points)
                if len(selected_points) == 4:
                    #perform perspective transformation and display result
                    warped_image = fourPointTransformation(display_image.copy(), np.array(selected_points))
                    cv2.imshow('Warped Image', warped_image)

    def fourPointTransformation(image, pts):
        #obtain consistent order of the points and unpack them individually
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        #compute width and height of new image
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        #create the desitnation points for perspective information
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 60, maxHeight - 200],
            [0, maxHeight - 1]], dtype='float32')

        #compute the perspective transofrmation matrix and apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    def order_points(pts):
        print('Original order', pts)
        #initialize a list of coordinates that will be ordered
        rect = np.zeros((4, 2), dtype='float32')

        #top-left point will have the smallest sum, while bottom-right will have largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        #top-right point will have smallest difference, while bottom-left point will have largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        print('Ordered points', rect)
        return rect

    #create main window
    root = tk.Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(title='Select an image',
                                            filetypes=[("Image Files", ".png .jpg .jpeg .bmp" )])

    if image_path !="":
        global display_image
        original_image = cv2.imread(image_path)
        height, width = original_image.shape[:2]
        scale = 600 / max(height, width)
        display_image = cv2.resize(original_image, None, fx=scale, fy=scale)
        dots = np.zeros_like(display_image)

        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", mouse_callback)
        while True:
            combined_image = cv2.addWeighted(display_image, 0.7, dots, 0.3, 0)
            cv2.imshow("Image", combined_image)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break

scan()
