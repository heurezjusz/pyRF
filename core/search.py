# search mode main functions

import config
import copy
import numpy as np
from core import calculate_rf, output_filename
from obspy.core.stream import Stream


def rotate_search(data):
    if config.VERBOSITY >= 2:
        print("looking for azimuth")

    # looking for azimuth
    amin = config.AZIMUTH_ANGLES['min']
    amax = config.AZIMUTH_ANGLES['max']
    astep = config.AZIMUTH_ANGLES['step']
    azimuth = amin + astep * np.argmax([_sum_of_amplitudes(copy.deepcopy(data), a * astep)
                                        for a in range(int(amin / astep), int(amax / astep) + 1)])

    # looking for inclination
    imin = config.INCLINATION_ANGLES['min']
    imax = config.INCLINATION_ANGLES['max']
    istep = config.INCLINATION_ANGLES['step']
    inclination = imin
    prev = None
    for i in range(int(imin / istep), int(imax / istep) + 1):
        inci = i * istep
        val = _rms(copy.deepcopy(data), azimuth, inci)
        if prev and prev < val:
            inclination = inci
            break
        prev = val

    if config.VERBOSITY >= 1:
        print("azimuth angle: %f inclination angle: %f" % (azimuth, inclination))

    data.rotate('ZNE->LQT', azimuth, inclination)
    return data


def _sum_of_amplitudes(data, azimuth):
    if config.VERBOSITY >= 3:
        print("analyzing data for azimuth=%f" % (azimuth))
    data.rotate('ZNE->LQT', azimuth, 0)

    data = calculate_rf(data, filter_config=config.SEARCH_FILTER_FREQ,
                        time_from = 0, time_to = 2)

    rfQ = data.select(component='Q')
    return np.sum(rfQ.traces[0].data)


def _rms(data, azimuth, inclination):
    if config.VERBOSITY >= 3:
        print("analyzing data for inclination=%f" % inclination)
    data.rotate('ZNE->LQT', azimuth, inclination)

    data = calculate_rf(data, filter_config=config.SEARCH_FILTER_FREQ,
                        time_from = -2, time_to = 0)

    rfQ = data.select(component='Q')
    return np.sum(rfQ.traces[0].data ** 2)