# theoretical mode main functions

import config
from core import calculate_rf, deconvolve, station_event
from external import collect_data

def rotate_theoretical(data, filename):
    if config.VERBOSITY >= 2:
        print("rotate: counting theoretical azimuth and inlcination")
    
    azimuth, slowness, V_S = _collect_data(filename)
    inci = _theoretical_inclination(slowness, V_S)
    data.rotate('ZNE->LQT', azimuth, inci)
    return data


import math
def _theoretical_inclination(slowness, V_S):
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


def _collect_data(filename):
    station, _ = station_event(filename)
    V_S = config.VS_STAION.get(station)
    if V_S is None:
        V_S = config.VS_DEFAULT

    if config.COLLECTDATA_MODE == "manual":
        azi, slow = config.AZIMUTH, config.SLOWNESS

    elif config.COLLECTDATA_MODE == "find":
        azi, slow = collect_data(filename)

    else:
        raise NotImplementedError

    return azi, slow, V_S