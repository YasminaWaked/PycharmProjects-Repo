import cv2
import numpy as np

drawing = False
points = []
mask = None

def simple_lasso():
    clone = image.copy()
    (x1, y1, x2, y2) = cv2.selectROI("Select Rectangular Area", image, fromCenter=False, showCrosshair=True)
    selected_area = clone[y1:y1 + y2, x1:x1 + x2]
    cv2.imshow("Selected Rectangular Area", selected_area)

def draw_freehand(event, x, y, flags, param):
    global drawing, points

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        points.append((x, y))
        cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            print(x, y)
            points.append((x, y))

def freehand_lasso():
    global mask
    mask = np.zeros_like(image)

    cv2.namedWindow("Freehand Selection")
    cv2.setMouseCallback("Freehand Selection", draw_freehand)

    while True:
        cv2.imshow("Freehand Selection", cv2.addWeighted(image, 0.7, mask, 0.3, 0))
        key = cv2.waitKey(1) & 0xFF

        if key == ord('x'): #press x to restart selection
            mask = np.zeros_like(image)
        elif key == 27: #pres esc to submit selection
            break

    selected_area = cv2.bitwise_and(image, mask)
    cv2.imwrite('saved_image.jpg', selected_area)
    cv2.imshow("Freehand Selected Area", selected_area)

def color_based_lasso(image):
    #define the lower and upper threshold for the color 'white'
    lower_white = np.array([0, 0, 150])
    upper_white = np.array([180, 50, 255])

    #convert original RGB image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #create binar mask
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    #extract selected region
    selected_area = cv2.bitwise_and(image, image, mask=mask)

    #display original and selected image
    cv2.imshow("Original Image", image)
    cv2.imshow("Selected Area", selected_area)


if __name__ == '__main__':
    image_path = 'flower.jpeg'
    image= cv2.imread(image_path)

    #simple_lasso()
    #freehand_lasso()
    color_based_lasso(image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
