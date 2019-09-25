import os
import time


def init_grid(ingrid=None, **kwargs):
    val = kwargs['val']
    w = kwargs['w']
    h = kwargs['h']
    return [[val for x in range(w)] for y in range(h)]


def idgrid(ingrid, **kwargs):
    return ingrid


def addgrid(ingrid, **kwargs):
    d = kwargs['d']
    return [[v + d for v in yrow] for yrow in ingrid]


def mingrid(ingrid, **kwargs):
    upper = kwargs['upbnd']
    return [[min(v, upper) for v in yrow] for yrow in ingrid]


def maxgrid(ingrid, **kwargs):
    lower = kwargs['lobnd']
    return [[min(v, lower) for v in yrow] for yrow in ingrid]


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
