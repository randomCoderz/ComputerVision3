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
                from_pixel = [i, j]
                if is_outer:
                    nbd += 1
                    from_pixel = [i, j - 1]
                    border = outer
                    # if root[lnbd] == outer:
                    #     # TODO borderPrime parent
                    #     print("borderPrime_parent_outer")
                    # elif root[lnbd] == hole:
                    #     # TODO borderPrime
                    #     print("borderPrime_outer")
                else:
                    nbd += 1
                    if img[i, j] > 1:
                        lnbd = img[i, j]
                    from_pixel = [i, j + 1]
                    border = hole
                    # if root[lnbd] == outer:
                    #     # TODO borderPrime
                    #     print("borderPrime_outer")
                    # elif root[lnbd] == hole:
                    #     # TODO borderPrime parent
                    #     print("borderPrime_parent_hole")
                to_pix = [i, j]
                img = step3(img, to_pix, from_pixel, nbd)
        # Step 4
        if img[i, j] != 0 and img[i, j] != 1:
            lnbd = abs(img[i][j])
    return img


def translation(to_translate, current_pixel):
    i, j = current_pixel[0], current_pixel[1]
    i, j = i + to_translate[0], j + to_translate[1]
    return i, j


# find direction between two given pixels
def get_start_position(to_dir, from_dir):
    return from_dir[0] - to_dir[0], from_dir[1] - to_dir[1]


def step3(img, current_pixel, from_pixel, nbd):
    # Create a "circular array", we will use this to help iterate clockwise, counterclockwise
    coord_map = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    # Translate the current pixel values to match the circular array format
    moved = get_start_position(current_pixel, from_pixel)
    # 3.1
    p1 = (0, 0)
    for i in range(8):
        try:
            # Comparing values, so get the actual value on the actual coordinate
            pix_translated = translation(moved, current_pixel)
            # Get actual value, not the coor_map
            newp = img[pix_translated[0], pix_translated[1]]
            # Check to see if that point's value is equal to zero
            if newp != 0:
                p1 = moved[0], moved[1]
                break
            moved = clockwise(coord_map, moved)
        except IndexError:
            pass

    if p1 == (0, 0):
        return

    # 3.2
    # set i1, j1 = i2,j2
    p2 = translation(p1, current_pixel)
    # set i3, j3 = i, j
    p3 = current_pixel[0], current_pixel[1]
    moved = get_start_position(p3, p2)
    for counter in range(8):
        # 3.3
        p4 = (0, 0)
        pix_translated = translation(moved, current_pixel)
        p4_actual_val = img[pix_translated[0], pix_translated[1]]
        if p4_actual_val != 0:
            p4 = moved[0], moved[1]
        # 3.4
        if img[p3[0], p3[1] + 1] == 0:
            img[p3[0], p3[1]] = -nbd
        if img[p3[0], p3[1] + 1] != 0 and img[p3[0], p3[1]] == 1:
            img[p3[0], p3[1]] = nbd
        # 3.5
        if p4 == current_pixel and p3 == p2:
            break
        p2 = p3
        p3 = p4
        moved = counterclockwise(coord_map, moved)
    return img


# Move clockwise around pixel
def clockwise(coord_map, point):
    next_index = coord_map.index(point) + 1
    leng = len(coord_map) - 1
    if next_index > leng:
        next_index = 0
    return coord_map[next_index]


# Move counterclockwise around the pixel
def counterclockwise(coord_map, point):
    next_index = coord_map.index(point) - 1
    if next_index < 0:
        next_index = 7
    return coord_map[next_index]


def open_cv_contour(image):
    ret, thres = cv.threshold(image, 0, 1, cv.THRESH_BINARY)
    print("Thres: ", thres)
    # Get contour
    bin_image, contour, hierarchy = cv.findContours(thres, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    print("Contour: \n",  contour)
    print("Hierarchy: \n", hierarchy)


if __name__ == "__main__":
    toy_img = np.array([[1, 1, 1, 1, 1, 1, 1, 0, 0],
                        [1, 0, 0, 1, 0, 0, 1, 0, 1],
                        [1, 0, 0, 1, 0, 0, 1, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 0, 0]], np.uint8)
    open_cv_contour(toy_img)
    step1(toy_img)

