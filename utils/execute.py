import config
import copy
import numpy as np
from utils import rotate_theoretical, deconvolve, output_filename
from obspy.core.stream import Stream


def _calculate_rf(data, filter_config = {'FREQMIN': config.FREQMIN, 'FREQMAX': config.FREQMAX}, zero_s = 0):
    """
        input:
        [data] - obspy.core.stream.Stream object with event in LQT format.
            After function input [data] may be changed.
        [filter_config] (optional) - Python dictionary with keys 'FREQMIN' and 'FREQMAX',
            used in ObsPy 'boundpass' filter function.
        [zero] (optional) - "zero" moment is set [zero_s] seconds after beggining of the window.
            Default value is 0. (float)
        
        output: obspy.core.stream.Stream object containing
            calculated reveival function
    """

    # filtering 
    data = data.filter('bandpass', freqmin=filter_config['FREQMIN'], freqmax=filter_config['FREQMAX'])

    # normalization
    if config.NORMALIZE_BEFORE:
        mx = max([np.max(t.data) for t in data.traces])
        mn = min([np.min(t.data) for t in data.traces])
        for tr in data.traces:
            tr.data /= mx - mn

    # counting receival function
    stL = data.select(component='L')
    stQ = data.select(component='Q')
    stT = data.select(component='T')

    rfQ, rfT, rfL = deconvolve([stQ.traces[0].data, stT.traces[0].data, stL.traces[0].data], stL.traces[0].data)
    if config.REVERSE_QRF: rfQ = -rfQ
    if config.REVERSE_TRF: rfT = -rfT

    # setting "zero" moment
    zero_pos = np.argmax(rfL)
    freq = int(1 / stL.traces[0].stats['delta'])
    if zero_pos < zero_s * freq:
        rfQ = np.concatenate(np.zeros(zero * freq - zero_pos), rfQ)
        rfT = np.concatenate(np.zeros(zero * freq - zero_pos), rfT)

    stQ.traces[0].data = rfQ[zero_pos - zero_s * freq : ]
    stT.traces[0].data = rfT[zero_pos - zero_s * freq : ]

    data = Stream(stQ.traces + stT.traces)
    
    # normalization
    if config.NORMALIZE_AFTER:
        mx = max([np.max(t.data) for t in data.traces])
        mn = min([np.min(t.data) for t in data.traces])
        for tr in data.traces:
            tr.data /= mx - mn

    return data


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