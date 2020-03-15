import cv2 as cv
import numpy as np


def main_func():
    image = cv.imread('fig1.jpg', 0)
    # Bitwise operation on the figure to invert color
    img = cv.bitwise_not(image)
    ret, thres = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    # Get contour
    bin_image, contour, hierarchy = cv.findContours(thres, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # Define the new image size and fill it with zeros
    final_img = np.zeros([35, 43], dtype=int)
    # Set x and y scale
    scale_x = 35/812
    scale_y = 43/639
    for i in range(len(contour)):
        m = cv.moments(contour[i])
        if m['m00'] == 0:
            # Avoid divide by zero error
            continue
        else:
            new_x = int((m['m01']/m['m00']) * scale_x)
            new_y = int((m['m10']/m['m00']) * scale_y)
            final_img[new_x, new_y] = 255

    cv.imwrite('Final.jpg', final_img)


if __name__ == "__main__":
    main_func()


