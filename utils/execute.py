import config
import copy
import numpy as np
from utils import rotate_theoretical, deconvolve, output_filename
from obspy.core.stream import Stream


def _calculate_rf(data):
    # filtering 
    data = data.filter('bandpass', freqmin=config.FREQMIN, freqmax=config.FREQMAX)

    # normalization
    if config.NORMALIZE_BEFORE:
        maxes = data.max()
        for i in range(len(maxes)):
            data.traces[i].data /= maxes[i]

    # counting receival function
    stL = data.select(component='L')
    stQ = data.select(component='Q')
    stT = data.select(component='T')

    RFtraces = deconvolve([stQ.traces[0].data, stT.traces[0].data], stL.traces[0].data)
    if config.REVERSE_QRF: RFtraces[0] = -RFtraces[0]
    if config.REVERSE_TRF: RFtraces[1] = -RFtraces[1]
    stQ.traces[0].data = RFtraces[0]
    stT.traces[0].data = RFtraces[1]

    data = Stream(stQ.traces + stT.traces)
    
    # normalization
    if config.NORMALIZE_BEFORE:
        maxes = data.max()
        for i in range(len(maxes)):
            data.traces[i].data /= maxes[i]

    return data


def execute_theoretical(data):
    # rotating
    data = rotate_theoretical(data)

    if config.SAVE_ROTATED:
        data.write(output_filename(datafile, prefix='rotated_'), config.SAVE_FORMAT)
    if config.PLOT_ROTATED: data.plot()
    
    return _calculate_rf(data)


def _sum_of_amplitudes(data, azim, incli):
    if config.VERBOSITY >= 3:
        print("analyzing data for azimuth=%d, inclination=%d" % (azim, incli))
    data.rotate('NE->RT', azim, 0)
    data.filter('bandpass', freqmin=config.FREQMIN, freqmax=config.FREQMAX)

    stR = data.select(component='R')
    stZ = data.select(component='Z')
    rfR = deconvolve([stR.traces[0].data], stZ.traces[0].data)[0]
    
    mx_pos = np.argmax(rfR)
    freq = int(1 / stR.traces[0].stats['delta'])
    return np.max(rfR[mx_pos : mx_pos + freq]) - np.min(rfR[mx_pos : mx_pos + freq])
    
    

def execute_search(data):
    if config.VERBOSITY >= 2:
        print("looking for azimuth")
    azimuth = np.argmax([_sum_of_amplitudes(copy.deepcopy(data), a, 0) for a in range(360)])
    incli = np.argmax([_sum_of_amplitudes(copy.deepcopy(data), azimuth, i / 2.) for i in range(0, 181)])
    if config.VERBOSITY >= 1:
        print("azimuth angle: %d inclination angle: %d" % (azimuth, incli))
        
    data.rotate('ZNE->LQT', azimuth, incli)

    if config.SAVE_ROTATED:
        data.write(output_filename(datafile, prefix='rotated_'), config.SAVE_FORMAT)
    if config.PLOT_ROTATED: data.plot()
    
    return _calculate_rf(data)