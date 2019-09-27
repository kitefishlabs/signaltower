import cv2 as cv
import numpy as np

bthresh = 0.18

path_off = 'imgs/001.jpg'
path_on = 'imgs/002.jpg'

img0 = cv.imread(path_off)
img1 = cv.imread(path_on)

white = (255, 255, 255)


def subc(rgb, a):
    return ((rgb[0] - a), (rgb[1] - a), (rgb[2] - a))


mask_left = 180
mask_cellw = 105
mask_top = 280
mask_cellh = 65


def get_brightness_scores(img0, img1):
    blurred0 = cv.GaussianBlur(img0, (19, 19), 10)
    blurred1 = cv.GaussianBlur(img1, (19, 19), 10)
    diff = cv.subtract(blurred1, blurred0)
    mask = np.zeros(img0.shape[:2], np.uint8)

    res = []
    decisions = []

    for r in range(9):
        for c in range(5):
            mask[:] = 0.0
            mask[(mask_top + (mask_cellh * r)): (mask_top + (mask_cellh * (r + 1))),
                 (mask_left + (mask_cellw * c)):(mask_left + (mask_cellw * (c + 1)))] = 255
            masked_img = cv.bitwise_and(diff, diff, mask=mask)
            cv.imwrite('imgs/mask' + '_' + str(r) + '_' +
                       str(c) + '_' + '.jpg', masked_img)
            x0 = mask_left + (mask_cellw * c)
            y0 = mask_top + (mask_cellh * r)
            cv.line(diff, (mask_left, y0),
                    (mask_left + (5 * mask_cellw), y0), white)
            cv.line(diff, (x0, mask_top),
                    (x0, mask_top + (9 * mask_cellh)), white)

            res += [np.average(masked_img)]

    decisions = sorted([(a, b) for (a, b) in enumerate(res)
                        if b > bthresh], key=(lambda x: x[1]))
    cv.imwrite('imgs/res.jpg', diff)
    return (res, decisions)
