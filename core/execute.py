import config
import copy
import numpy as np
from utils import rotate_theoretical, deconvolve, output_filename
from obspy.core.stream import Stream


def execute_theoretical(data, datafile):
    # rotating
    data = rotate_theoretical(data)

    if config.SAVE_ROTATED:
        data.write(output_filename(datafile, prefix='rotated_'), config.SAVE_FORMAT)
    if config.PLOT_ROTATED: data.plot()
    
    return _calculate_rf(data)


def _sum_of_amplitudes(data, azimuth):
    if config.VERBOSITY >= 3:
        print("analyzing data for azimuth=%f" % (azimuth))
    data.rotate('ZNE->LQT', azimuth, 0)

    data = _calculate_rf(data)

    rfQ = data.select(component='Q')
    freq = int(1 / rfQ.traces[0].stats['delta'])
    return np.sum(rfQ.traces[0].data[ : 2 * freq])


def _rms(data, azimuth, inclination):
    if config.VERBOSITY >= 3:
        print("analyzing data for inclination=%f" % inclination)
    data.rotate('ZNE->LQT', azimuth, inclination)

    data = _calculate_rf(data, zero_s = 2)

    rfQ = data.select(component='Q')
    freq = int(1 / rfQ.traces[0].stats['delta'])
    result = rfQ.traces[0].data[ : 2 * freq]
    return np.sum(result ** 2)


def execute_search(data, datafile):
    if config.VERBOSITY >= 2:
        print("looking for azimuth")

    amin = config.AZIMUTH_ANGLES['min']
    amax = config.AZIMUTH_ANGLES['max']
    astep = config.AZIMUTH_ANGLES['step']
    azimuth = amin + astep * np.argmax([_sum_of_amplitudes(copy.deepcopy(data), a * astep)
                                        for a in range(int(amin / astep), int(amax / astep) + 1)])

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

    if config.SAVE_ROTATED:
        data.write(output_filename(datafile, prefix='rotated_'), config.SAVE_FORMAT)
    if config.PLOT_ROTATED: data.plot()
    
    return _calculate_rf(data)