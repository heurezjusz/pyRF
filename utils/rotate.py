import config

def rotate(data, mode="theoretical"):
    if mode not in [ "theoretical", "search" ]:
        raise NotImplementedError
    #TODO : check data
    if mode == "theoretical":
        return _rotate_theoretical(data)
    if mode == "seatch":
        return _rotate_search(data)


def _rotate_theoretical(data):
    theoretical = _theoretical_azimuth(config.SLOWNESS, 1.3)
    return data.rotate('ZNE->LQT', config.AZIMUTH, theoretical)

import math
def _theoretical_azimuth(slowness, V_S = 6. / math.sqrt(3)):
    """Arguments:
        slowness - some constant from file in [seconds / degrees]
        V_S - average velocity of S-waves in shell
       Result:
        Value of theoretical azimuth given in degrees
    """

    c = math.sqrt(1. / (V_S ** 2) - slowness ** 2)
    d = 2 * (V_S ** 2) * slowness * c
    e = 1. - 2 * (V_S ** 2) * (slowness ** 2)
    return math.atan(d / e) * 180 / math.pi


def _rotate_search(data):
    pass