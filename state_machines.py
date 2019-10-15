import os
import time
import random

import io
# import picamera
import cv2
import numpy as np
# from imutils.video import VideoStream
# import imutils

ROWS = 9
COLS = 5


# def routes = {
#     0: []
# }

def get_(kwargs, key='val', default=None):
    try:
        return kwargs[key]
    except KeyError:
        return default


def init_grid(ingrid=None, **kwargs):
    val = get_(kwargs, 'val', 127)
    return [val for x in range(ROWS * COLS)]


def idgrid(ingrid, **kwargs):
    return ingrid


def grid_allon(ingrid, **kwargs):
    val = get_(kwargs, 'val', 127)
    return [val for i in range(ROWS * COLS)]


def grid_alloff(ingrid, **kwargs):
    return [0 for i in range(ROWS * COLS)]


def grid_set(ingrid, **kwargs):
    val = get_(kwargs, 'val', 127)
    return [val for i in range(ROWS * COLS)]


def grid_setone(ingrid, **kwargs):
    val = get_(kwargs, 'val', 127)
    i = get_(kwargs, 'i')
    if i is not None:
        ingrid[i] = val
    else:
        print("warning: attempting to assign value where i == None; i:", i)
    return ingrid


def grid_add(ingrid, **kwargs):
    d = get_(kwargs, 'd', 1)
    return [min(max((val + d), 0), 127) for val in ingrid]


def grid_min(ingrid, **kwargs):
    lower = min(max(get_(kwargs, 'lobnd', 0), 0), 127)
    return [max(val, lower) for val in ingrid]


def grid_max(ingrid, **kwargs):
    upper = min(max(get_(kwargs, 'upbnd', 127), 0), 127)
    return [min(val, upper) for val in ingrid]


def produce_one_random(lower, upper):
    return random.randint(lower, upper)


def grid_random(ingrid=None, **kwargs):
    lower = min(max(get_(kwargs, 'lobnd', 0), 0), 127)
    upper = min(max(get_(kwargs, 'upbnd', 127), 0), 127)
    if ingrid is not None:
        return [produce_one_random(lower, upper) for val in ingrid]
    else:
        res = init_grid(**{'val': 0})
        return [produce_one_random(lower, upper) for val in res]


def grid_random_single_point(ingrid, **kwargs):
    lower = min(max(get_(kwargs, 'lobnd', 0), 0), 127)
    upper = min(max(get_(kwargs, 'upbnd', 127), 0), 127)
    clear = get_(kwargs, 'clear', False)
    random_i = random.randint(0, ((COLS * ROWS) - 1))
    if clear:
        res = grid_alloff(ingrid)
    else:
        res = ingrid
    try:
        res[random_i] = produce_one_random(lower, upper)
    except IndexError:
        print("grid_random_single_point failed for index: ", random_i)
    return res


def grid_random_toggle_point(ingrid, **kwargs):
    lobnd = min(max(get_(kwargs, 'lobnd', 0), 0), 128)
    upbnd = max(min(get_(kwargs, 'upbnd', 127), 128), 0)
    random_pt = random.randint(lobnd, upbnd)
    res = ingrid
    if res[random_pt] > 0:
        res[random_pt] = 0
    else:
        try:
            res[random_pt] = random.randint(lobnd, upbnd - 1)
        except IndexError:
            print(
                "there was an index error in grid_random_toggle_point (r,c): (", r, ", ", c, ")")
            pass
    return res


def chase(ingrid, **kwargs):
    direction = 0
    kwargs = kwargs['kwargs']
    direction = kwargs['dir']
    resi = 0
    for i in range(45):
        if (ingrid[int(i / 5)][i % 5] > 0):
            resi = i
            break
    print('resi: ', resi)
    resr = int(resi / 5)
    resc = resi % 5

    val = ingrid[resr][resc]
    ingrid[resr][resc] = 0

    if (direction == 0):

        if (resr % 2) == 0:
            if resc < 4:
                r = resr
                c = resc + 1
            else:
                r = resr + 1
                c = resc
        else:
            if resc > 0:
                r = resr
                c = resc - 1
            else:
                r = resr + 1
                c = resc

    elif (direction == 1):

        if (resr % 2) == 0:
            if resc > 0:
                r = resr
                c = resc - 1
            else:
                r = resr - 1
                c = resc
        else:
            if resc < 4:
                r = resr
                c = resc + 1
            else:
                r = resr - 1
                c = resc

    elif (direction == 2):

        if (resc % 2) == 0:
            if resr < 8:
                r = resr + 1
                c = resc
            else:
                r = resr
                c = resc + 1
        else:
            if resr > 0:
                r = resr - 1
                c = resc
            else:
                r = resr
                c = resc + 1

    else:

        if (resc % 2) == 0:
            if resr > 0:
                r = resr - 1
                c = resc
            else:
                r = resr
                c = resc - 1
        else:
            if resr < 8:
                r = resr + 1
                c = resc
            else:
                r = resr
                c = resc - 1

    if r < 0 or c < 0:
        # ingrid[8][4] = val
        return 44

    elif r > 8 or c > 4:
        # ingrid[0][0] = val
        return 0
    else:
        # ingrid[r][c] = val
        return (r * 9) + c

    # return ingrid


def grid_mirror(ingrid, **kwargs):
    kwargs = kwargs['kwargs']
    bthresh = kwargs['bthresh']
    nrows = kwargs['nrows']
    ncols = kwargs['ncols']
    gtop = kwargs['gtop']
    gleft = kwargs['gleft']
    gheight = kwargs['gheight']
    gwidth = kwargs['gwidth']
    vs = kwargs['vs']
    mask = kwargs['mask']
    # grab the next frame from the stream
    frame = kwargs['vs'].read()

    # quit if there was a problem grabbing a frame
    if frame is None:
        return ingrid

    # resize the frame and convert the frame to grayscale
    frame = imutils.resize(frame, width=200)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # if the frame dimensions are empty, set them
    # if W is None or H is None:
    # (H, W) = frame.shape[:2]

    res_ = [[0 for val in range(5)] for row in range(9)]
    res = []
    decisions = []

    for r in range(nrows):
        for c in range(ncols):
            mask[:] = 0.0
            mask[(gtop + (gheight * r)): (gtop + (gheight * (r + 1))),
                 (gleft + (gwidth * c)): (gleft + (gwidth * (c + 1)))] = 255
            masked_img = cv2.bitwise_and(gray, gray, mask=mask)
            res += [np.average(masked_img)]

            decisions = sorted([(a, b) for (a, b) in enumerate(
                res) if b > bthresh], key=(lambda x: x[0]))
    print("")
    print(decisions)
    print("")

    for dec in decisions:
        idx = dec[0]
        r = int(idx / 5)
        c = idx % 5
        res_[r][c] = 127

    return res_


class GridState:

    def __init__(self, **params):
        self.initialize(params)

    def initialize(self, params=None):
        self._check_cf_params(params)
        self.runstart = int(time.time())
        self.w = self.params['gridw']
        self.h = self.params['gridh']
        self.grid = None
        self.grid = self.grid_apply_f(
            init_grid, **{'w': self.w, 'h': self.h, 'val': 0})

    def _check_cf_params(self, params=None):
        """
        Simple mechanism to read in default parameters while substituting custom parameters.
        """
        self.params = params if params is not None else self.params
        dcfp = self.default_cf_params()
        for k in dcfp.keys():
            if k == 'log_file_path':
                self.params[k] = os.path.abspath(
                    self.params.get(k, dcfp[k]))
            else:
                self.params[k] = self.params.get(k, dcfp[k])
        return self.params

    @staticmethod
    def default_cf_params():
        params = {
            'verbose': False,			# useful for debugging
            # default file
            # 'log_file_path': os.path.abspath('run_' + str(self.runstart) + '.log'),
            'gridw': 5,
            'gridh': 9
        }
        return params

    def grid_apply_f(self, f, **kwargs):
        self.grid = f(self.grid, **kwargs)
        return self.grid
