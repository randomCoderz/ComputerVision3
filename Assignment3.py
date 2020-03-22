import cv2 as cv
import numpy as np


# NBD: stores a uniquely sequential number to the newly found border
# LNBD: stores the sequential number of the (outer or hole) border encountered most recently


def step1(img):
    nbd = 1
    lnbd = 1
    hole = "hole"
    outer = "outer"
    root = {lnbd: hole}
    # Get width of image
    width = np.size(img, 1)
    for i in range(len(img[0])):
        lnbd = 1
        for j in range(len(img[1])):
            # Check if there is outer
            is_outer = img[i, j] == 1 and (j == 0 or img[i, j-1] == 0)
            # Check if there is a hole
            is_hole = img[i, j] >= 1 and (j == width - 1 or img[i, j+1] == 0)
            if is_outer or is_hole:
                border = []
                from_pixel = img[i, j]
                if is_outer:
                    nbd += 1
                    from_pixel = img[i, j - 1]
                    border = outer
                    if root[lnbd] == outer:
                        # TODO borderPrime parent
                        print("borderPrime_parent_outer")
                    elif root[lnbd] == hole:
                        # TODO borderPrime
                        print("borderPrime_outer")
                else:
                    nbd += 1
                    if img[i, j] > 1:
                        lnbd = img[i, j]
                    from_pixel = img[i, j + 1]
                    border = hole
                    if root[lnbd] == outer:
                        # TODO borderPrime
                        print("borderPrime_outer")
                    elif root[lnbd] == hole:
                        # TODO borderPrime parent
                        print("borderPrime_parent_hole")
                step3(img, img[i, j], from_pixel, nbd)
            # Step 4
            if img[j, i] != 0 and img[j, i] != 1:
                lnbd = abs(img[i][j])
            return lnbd


def move(pixel, img, direct, dir_delta):
    newp = pixel + dir_delta[direct]
    width, height = img.size
    if(0 < newp[1] <= height) and (0 < newp[2] <= width):
        if img[newp] != 0:
            return newp
    return 0


# find direction between two given pixels
def get_direction(from_dir, to_dir, delta_dir):
    delta = to_dir - from_dir
    for i in range(delta_dir):
        if delta == delta_dir[i]:
            return delta_dir[i]
    return [None]


def step3(img, from_pixel, to_pixel, nbd):
    dir_delta = [np.indices((-1, 0)), np.indices((-1, 1)), np.indices((0, 1)), np.indices((1, 1)),
                 np.indices((1, 0)), np.indices((1, -1)), np.indices((0, -1)), np.indices((-1, -1))]
    direction = get_direction(from_pixel, to_pixel, dir_delta)
    moved = clockwise(direction)
    while moved != direction:
        new_pixel = move(from_pixel, img, moved, dir_delta)


def clockwise(direction):
    return (direction % 8) + 1


def counterclockwise(direction):
    return ((direction + 6) % 8) + 1


if __name__ == "__main__":
    toy_img = np.array([[1, 1, 1, 1, 1, 1, 1, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 0, 0]], np.uint8)

    step1(toy_img)
