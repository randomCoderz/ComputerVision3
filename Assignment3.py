import cv2 as cv
import numpy as np


# NBD: stores a uniquely sequential number to the newly found border
# LNBD: stores the sequential number of the (outer or hole) border encountered most recently

def step1(img):
    nbd = 1
    for i in range(img[0]):
        lnbd = 1
        for j in range(img[1]):
            # Get width of image
            width, height = img.size
            # Check if there is outer
            is_outer = img[i, j] == 1 and (j == 0 or img[i, j-1] == 0)
            # Check if there is a hole
            is_hole = img[i, j] >= 1 and (j == width - 1 or img[i, j+1] == 0)
            if is_outer or is_hole:
                border = []
                border_prime = []
                from_pixel = [j, i]
                if is_outer:
                    nbd += 1
                    from_pixel[j] -= 1

                else:
                    nbd += 1
                    if img[j, i] > 1:
                        lnbd = img[j, i]
                    from_pixel[j] += 1

            # Step 4
            if img[j, i] != 0 and img[j, i] != 1:
                lnbd = abs(img[i][j])
            return lnbd


if __name__ == "__main__":
    image = cv.imread('fig1.jpg')
    step1(image)
