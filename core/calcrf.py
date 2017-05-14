# function counting receival function

import numpy as np
from obspy.core.stream import Stream
import config
from core import deconvolve

def calculate_rf(data, filter_config = {'FREQMIN': config.FREQMIN, 'FREQMAX': config.FREQMAX}, zero_s = 0):
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
