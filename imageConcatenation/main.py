import cv2
import os

def combine_vertically(image1, image2):

    if image1 is None or image2 is None:
        print("Error: Unable to load images.")
    else:
        print("Height of image1: ", image1.shape[0])
        print("Width of image1: ", image1.shape[1])
        print("Height of image2: ", image2.shape[0])
        print("Width of image2: ", image2.shape[1])

        image1 = cv2.resize(image1, (image1.shape[1]//2, image1.shape[0]//2))
        image2 = cv2.resize(image2, (image2.shape[1]//2, image2.shape[0]//2))

        v_combined = cv2.vconcat([image1, image2])
        return v_combined

def combine_horizontally(image1, image2):
    if image1 is None or image2 is None:
        print("Error: Unable to load images.")
    else:
        print("Height of image1: ", image1.shape[0])
        print("Width of image1: ", image1.shape[1])
        print("Height of image2: ", image2.shape[0])
        print("Width of image2: ", image2.shape[1])

        image1 = cv2.resize(image1, (image1.shape[1]//2, image1.shape[0]//2))
        image2 = cv2.resize(image2, (image2.shape[1]//2, image2.shape[0]//2))

        h_combined = cv2.hconcat([image1, image2])
        return h_combined


def overlay(image1, image2, beta):
    print("Height of image1: ", image1.shape[0])
    print("Width of image1: ", image1.shape[1])
    print("Height of image2: ", image2.shape[0])
    print("Width of image2: ", image2.shape[1])

    image1 = cv2.resize(image1, (image1.shape[1]//2, image1.shape[0]//2))
    image2 = cv2.resize(image2, (image2.shape[1]//2, image2.shape[0]//2))

    overlay = cv2.addWeighted(image1, 1 - beta, image2, beta, 0)
    return overlay

def transform(image1, image2):
    print("Height of image1: ", image1.shape[0])
    print("Width of image1: ", image1.shape[1])
    print("Height of image2: ", image2.shape[0])
    print("Width of image2: ", image2.shape[1])

    image1 = cv2.resize(image1, (image1.shape[1]//2, image1.shape[0]//2))
    image2 = cv2.resize(image2, (image2.shape[1]//2, image2.shape[0]//2))

    combined_image = image1
    for i in range(2, 12, 2):
        print(i/10)
        overlay2 = cv2.addWeighted(image1, 1 - i/10, image2, i/10, 0)
        combined_image = cv2.vconcat([combined_image, overlay2])

    return combined_image

if __name__ == '__main__':
    image1 = cv2.imread('flower.jpeg')
    image2 = cv2.imread('flower2.jpeg')

    #combined_image = combine_vertically(image1, image2)
    #combined_image = combine_horizontally(image1, image2)
    #combined_image = overlay(image1, image2, 0.5)

    combined_image = transform(image1, image2)

    cv2.imshow("Images", combined_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
