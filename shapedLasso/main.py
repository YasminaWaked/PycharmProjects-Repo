import cv2
import numpy as np

#global variables that store selected points
points = []
shapes = []
mask = []
dots = []

#mouse callback function to capture points for shapes
def mouse_callback(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONUP:
        points.append((x, y))
        cv2.circle(dots, (x, y), 5, (0, 0, 255), -1)

#load image for area selection
image_path = 'flower.jpeg'
image = cv2.imread(image_path)

mask = np.zeros_like(image)
dots = np.zeros_like(image)

cv2.namedWindow("Image")
cv2.setMouseCallback('Image', mouse_callback)

while True:
    combined_image = cv2.addWeighted(image, 0.7, mask, 0.3, 0)
    combined_image = cv2.addWeighted(combined_image, 0.7, dots, 0.3, 0)
    cv2.imshow('Image', combined_image)
    key = cv2.waitKey(1)

    #press x to reset points for new selection
    if key == ord('x'):
        points = []
        shapes = []
        mask = np.zeros_like(image)
        dots = np.zeros_like(image)

    #press c to draw circle
    elif key == ord('c'):
        if len(points) == 2:
            radius = int(cv2.norm(np.array(points[1]) - np.array(points[0])))
            cv2.circle(mask, points[0], radius, (255, 255, 255), -1)

            circle_points = cv2.ellipse2Poly(points[0], (radius, radius), 0, 0, 360, 1)
            shapes.append(circle_points)
            dots = np.zeros_like(image)
            points = []

    #press e to draw ellipse
    elif key == ord('e'):
        if len(points) == 5:
            center, axes, angle = cv2.fitEllipse(np.array(points))
            center = (int(center[0]), int(center[1]))
            axes = (int(axes[0]/2), int(axes[1]/2))
            angle = int(angle)
            cv2.ellipse(mask, center, axes, angle, 0, 360, (255, 255, 255), -1)

            ellipse_points = cv2.ellipse2Poly(center, axes, angle, 0, 360, 1)
            shapes.append(ellipse_points)
            dots = np.zeros_like(image)
            points = []

    #press p to draw polygon
    elif key == ord('p'):
        if len(points) >= 5:
            #draw a polygon using all selected points (polygonal selection)
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(mask, [pts], (255, 255, 255))
            shapes.append(pts)
            dots = np.zeros_like(image)
            points = []

    #press q to submit selection and quit
    elif key == ord('q'):
        break

cv2.fillPoly(mask, shapes, (255, 255, 255))
selected_area = cv2.bitwise_and(image, mask)

#save selected area of the shape
#cv2.imwrite("saved_image.jpg", selected_area)

#display selected area
cv2.imshow("Selected Area", selected_area)
cv2.waitKey(0)
cv2.destroyAllWindows()
