# theoretical mode main functions

import config
from core import calculate_rf, deconvolve
from external import collect_data

def rotate_theoretical(data):
    if config.VERBOSITY >= 2:
        print("rotate: counting theoretical azimuth and inlcination")
    
    azimuth, slowness = _collect_data()
    inci = _theoretical_inclination(slowness, 1.3)
    data.rotate('ZNE->LQT', azimuth, inci)
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


def _collect_data():
    if config.COLLECTDATA_MODE == "manual":
        return config.AZIMUTH, config.SLOWNESS

    elif config.COLLECTDATA_MODE == "find":
        return collect_data()

    else:
        raise NotImplementedError