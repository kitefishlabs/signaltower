import os
import time
import random


def init_grid(ingrid=None, **kwargs):
    val = kwargs['val']
    w = kwargs['w']
    h = kwargs['h']
    return [[val for x in range(w)] for col in range(h)]


def idgrid(ingrid, **kwargs):
    return ingrid


def grid_allon(ingrid, **kwargs):
    try:
        val = kwargs['val']
    except KeyError:
        val = 255
    return [[val for x in row] for row in ingrid]


def grid_alloff(ingrid, **kwargs):
    return [[0 for x in row] for row in ingrid]


def grid_set(ingrid, **kwargs):
    val = kwargs['val']
    return [[val for x in row] for row in ingrid]


def grid_setone(ingrid, **kwargs):
    val = kwargs['val']
    r = kwargs['r']
    c = kwargs['c']
    ingrid[r][c] = val
    return ingrid


def grid_add(ingrid, **kwargs):
    d = kwargs['d']
    return [[val + d for val in row] for row in ingrid]


def grid_min(ingrid, **kwargs):
    upper = kwargs['upbnd']
    return [[min(val, upper) for val in row] for row in ingrid]


def grid_max(ingrid, **kwargs):
    lower = kwargs['lobnd']
    return [[max(val, lower) for val in row] for row in ingrid]


def grid_random(ingrid, **kwargs):
    lobnd = kwargs['lobnd']
    upbnd = kwargs['upbnd']
    return [[random.randint(lobnd, upbnd) for x in row] for row in ingrid]


def grid_random_single_point(ingrid, **kwargs):
    lobnd = kwargs['lobnd']
    upbnd = kwargs['upbnd']
    w = len(ingrid[0])
    h = len(ingrid)
    c = random.randint(0, w - 1)
    r = random.randint(0, h - 1)
    res = [[0 for x in row] for row in ingrid]
    res[r][c] = random.randint(lobnd, upbnd)
    return res


def grid_random_toggle_point(ingrid, **kwargs):
    lobnd = min(max(kwargs['lobnd'], 0), 255)
    upbnd = max(min(kwargs['upbnd'], 255), 0)
    w = len(ingrid)
    h = len(ingrid[0])
    val = random.randint(0, 1) * random.randint(lobnd, upbnd)
    c = random.randint(0, w - 1)
    r = random.randint(0, h - 1)
    res = ingrid
    try:
        res[r][c] = val
    except IndexError:
        print(c)
        print(r)
        print(val)
        return
    return res


def chase(ingrid, **kwargs):
    direction = 0
    direction = kwargs['dir']
    resi = kwargs['i']
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
        ingrid[8][4] = val

    elif r > 8 or c > 4:
        ingrid[0][0] = val
    else:
        ingrid[r][c] = val

    return ingrid


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
            init_grid, **{'w': self.w, 'h': self.h, 'val': 64})

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
