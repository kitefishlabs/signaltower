import cv2 as cv
import numpy as np

bthresh = 0.18

path_off = 'imgs/001.jpg'
path_on = 'imgs/002.jpg'

img0 = cv.imread(path_off)
img1 = cv.imread(path_on)

# out = np.zeros(img0.shape)

white = (255, 255, 255)


def subc(rgb, a):
    return ((rgb[0] - a), (rgb[1] - a), (rgb[2] - a))


def get_brightness_scores(img0, img1):
    blurred0 = cv.GaussianBlur(img0, (19, 19), 10)
    blurred1 = cv.GaussianBlur(img1, (19, 19), 10)
    diff = cv.subtract(blurred1, blurred0)
    mask = np.zeros(img0.shape[:2], np.uint8)

    res = []
    decisions = []

    for r in range(4):
        for c in range(4):
            mask[:] = 0.0
            mask[(180 + (105 * c)):(180 + (105 * (c + 1))),
                 (280 + (65 * r)): (280 + (65 * (r + 1)))] = 255
            masked_img = cv.bitwise_and(diff, diff, mask=mask)
            x0 = 180 + (105 * c)
            y0 = 280 + (65 * r)
            cv.line(diff, (180, y0), (600, y0), subc(white, (2*((r*4)+c))))
            cv.line(diff, (x0, 280), (x0, 600), subc(white, (2*((r*4)+c))))

            res += [np.average(masked_img)]

    decisions = sorted([(a, b) for (a, b) in enumerate(res)
                        if b > bthresh], key=(lambda x: x[1]))
    cv.imwrite('imgs/res.jpg', diff)
    return (res, decisions)
