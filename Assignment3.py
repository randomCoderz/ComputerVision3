import cv2 as cv
import numpy as np


# NBD: stores a uniquely sequential number to the newly found border
# LNBD: stores the sequential number of the (outer or hole) border encountered most recently

def step1(img):
    nbd = 1
    lnbd = 1
    final_img = np.zeros(img.shape)
    for i in range(img[0]):
        for j in range(img[1]):
            if img[i, j] == 1 and img[i, j-1] == 0:
                # Decide that the pixel (i,j) is the border,
                nbd += 1
                # increment i2,j2 <- (i, j-1)
            elif img[i, j] >= 1 and img[i, j+1] == 0:
                # Decide that the pixel is the (i,j) is the border following starting point of a hole border
                nbd += 1
                # (i2, j2) <- (i, j + 1)
                if img[i, j] > 1:
                    lnbd = img[i, j]
            else:
                lndb = step4(img, lnbd, i, j)
                continue
            # Step 2
            try:
                if img[i - 1, j + 1] > 0 or img[i, j + 1] > 0 or img[i + 1, j + 1] > 0 or img[i - 1, j] > 0 or img[i + 1, j] > 0 or img[i - 1, j - 1] > 0 or img[i, j - 1] > 0 or img[i + 1, j - 1] > 0:
                    print("")
            except IndexError:
                pass


def step4(img, lnbd, i, j):
    if img[i][j] != 1:
        lnbd = abs(img[i][j])
    return lnbd


if __name__ == "__main__":
    image = cv.imread('fig1.jpg')
    step1(image)
