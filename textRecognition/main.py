import cv2
import pytesseract

image = cv2.imread('whiteText.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
recognized_text = pytesseract.image_to_string(gray_image)

print('Recognized Text: ')
print(recognized_text)

image = cv2.imread('stopText.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
cv2.imshow('Binary Image', binary_image)

contours, _ = cv2.findContours(binary_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
image_with_contours = image.copy()
cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

cv2.imshow('Original Image', image)
cv2.imshow('Image with Contours', image_with_contours)

cv2.waitKey(0)
cv2.destroyAllWindows()
