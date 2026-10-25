import cv2
import numpy as np

color_ranges = {
    'orange': ([11, 100, 100], [25, 255, 255]),
    'yellow': ([26, 100, 100], [35, 255, 255]),
    'green': ([36, 100, 100], [80, 255, 255]),
    'blue': ([81, 100, 100], [130, 255, 255]),
    'purple': ([131, 100, 100], [160, 255, 255]),
    'pink': ([161, 100, 100], [175, 255, 255]),
    'red': ([176, 100, 100], [180, 255, 255]),
    'black': ([0, 0, 0], [180, 100, 50]),
    'white': ([0, 0, 200], [180, 20, 255]),
    'brown': ([0, 50, 50], [20, 255, 150]),
    'gray': ([0, 0, 25], [180, 25, 200])
}

def colorDetection():
    image_path = 'colors.jpg'
    image = cv2.imread(image_path)
    color = input('Input color to detect: ')

    def color_detection(image, lower_color, upper_color):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        result = cv2.bitwise_and(image, image, mask=mask)
        return result

    if color in color_ranges.keys():
        #perfeorm color detection. Parameters: image, lower range, upper range
        result = color_detection(image, np.array(color_ranges[color][0]), np.array(color_ranges[color][1]))

        cv2.imshow('Orignal Frame', image)
        cv2.imshow('Color Detected Frame', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print('invalid input')


def eyeDropper():
    def getColorName(hue_value):
        #function to get the color name based on hue value
        for color_name, (lower, upper) in color_ranges.items():
            if lower[0] <= hue_value <= upper[0]:
                return color_name
        return None

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            #get BGR color value of clicked pixel
            b, g, r = image[y, x] #blue green red clicked on imag x y coordinates
            print(f'Clicked pizel color: B{b}, G={g}, R={r}')

            #create a new window to display detected color
            color_window = np.zeros((100, 120, 3), dtype=np.uint8) #creates numpy array called color_window dimensions: 100x120 and 3 channels (BGR) initialised with zeros
            color_window[:, :] = (b, g, r)

            #show detected color in window
            cv2.imshow('Detected Color', color_window)

            #show color name
            hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            color_hue = hsv_frame[y, x, 0]
            color_name = getColorName(color_hue)
            if color_name:
                print(f'Color name: {color_name}')

    image = cv2.imread('colors.jpg')
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #colorDetection()
    eyeDropper()
