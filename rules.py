import numpy as np
import cv2 as cv

import matplotlib.pyplot as plt

# rules + constants
PANELH = 4
PANELW = 4

# state = N * N array of boolean (int: 0|1) )


def identity(prev_state, current_state):
    return current_state


def average(prev_state, current_state):
    # return [((a + b) / 2.0) for (a,b) in zip(prev_state, current_state)]
    a = prev_state
    b = current_state
    # print(a.shape)
    # print(b.shape)
    # assert a.shape[0] == 1
    # assert b.shape[0] == 1
    # assert a.shape == b.shape
    return np.mean(np.r_[a, b], axis=0)


def maxor(prev_state, current_state):
    # return [((a + b) / 2.0) for (a,b) in zip(prev_state, current_state)]
    a = prev_state
    b = current_state
    # assert a.shape[0] == 1
    # assert b.shape[0] == 1
    # assert a.shape == b.shape
    return np.max(np.r_[a, b], axis=0)


# TODO: change random params, ditributions?
def thresh(x): return x > 0.5


def lights_off(prev_state=None, current_state=None):
    return np.zeros(PANELH, PANELW, 1)


def lights_on(prev_state=None, current_state=None):
    return np.ones(PANELH, PANELW, 1)


def lights_dimmed(dim=128, prev_state=None, current_state=None):
    return (np.ones(PANELH, PANELW, 1) * (dim / 255.0))


def random_lights(prev_state=None, current_state=None):
    x = np.random.rand(PANELH, PANELW, 1)
    return thresh(x)                           # --> lights on and off


def show_lights(state=None):
    if state is not None:
        state = [[1.0 for x in y if x == True else 0.0] for y in state[:, :, 0]]
        print(state)
        plt.plot(state)
        plt.show()
