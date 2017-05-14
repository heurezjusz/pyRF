# theoretical mode main functions

import config
from core import calculate_rf, deconvolve

def rotate_theoretical(data):
    if config.VERBOSITY >= 2:
        print("rotate: counting theoretical azimuth and inlcination")
    inci = _theoretical_inclination(config.SLOWNESS, 1.3)
    data.rotate('ZNE->LQT', config.AZIMUTH, inci)
    return data


import math
def _theoretical_inclination(slowness, V_S = 6. / math.sqrt(3)):
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