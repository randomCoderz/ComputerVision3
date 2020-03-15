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
            # Decide that the pixel (i,j) is the border, increment i2,j2 <- (i, j-1)
            if img[i, j] == 1 and img[i, j-1] == 0:
                nbd += 1
                img[i + 1, j +1] = img[i, j - 1]
            # Decide that the pixel is the (i,j) is the border following starting point of a hole border, increment nbd
            # (i2, j2) <- (i, j + 1) and LNBD <- fij in case fij > 1
            elif img[i, j] >= 1 and img[i, j+1] == 0:
                nbd += 1
                img[i+1, j+1] = img[i, j+1]
                if img[i, j] > 1:
                    lnbd = img[i, j]
            else:
                lndb = step4(img, lnbd, i, j)
            step2()
            step3()


def step2():
    print("TODO")


def step3():
    print("TODO")


def step3_1():
    print("TODO")


def step3_2():
    print("TODO")


def step3_3():
    print("TODO")


def step3_4():
    print("TODO")


def step3_5():
    print("TODO")


def step4(img, lnbd, i, j):
    if img[i][j]:
        lnbd = abs(img[i][j])
    return lnbd


if __name__ == "__main__":
    image = cv.imread('fig1.jpg')
    step1(image)
