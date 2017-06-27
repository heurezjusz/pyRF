# python3 script counting receival function

__author__ = 'Patryk Czajka'

import numpy as np
from obspy.core.stream import Stream
import config
from core import deconvolve

def calculate_rf(data, filter_config = config.FILTER_FREQ, time_from = config.RF_TIME_FROM,
                 time_to = config.RF_TIME_TO, zero_shift = 0.):
    """
        input:
        [data] - obspy.core.stream.Stream object with event in LQT format.
            After function input [data] may be changed.
        [filter_config] (optional) - Python dictionary with keys 'FREQMIN' and 'FREQMAX',
            used in ObsPy 'boundpass' filter function.
        [time_from, time_to] (floats, optional)- result will contain data between
            [time_from] and [time_to] seconds. Time is measured from time 0.
        [zero_shift] (float, optional) - time 0 is set [zero_shift] seconds after theoretical
            time 0 (maximum in deconvolved L trace).
            Default value is 0. (float)
        [zero_date] (obspy.core.utcdatetime.UTCDateTime or convertable, optional)
            - time 0 is represented as [zero_date] time
        
        output: obspy.core.stream.Stream object containing
            calculated reveival function
    """
    assert time_from < time_to
    zero_date = _get_zero_date(data)

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
    freq = int(1 / stL.traces[0].stats['delta'])
    zero_pos = np.argmax(rfL) + int(freq * zero_shift)
    from_pos = zero_pos + int(time_from * freq)
    to_pos = zero_pos + int(time_to * freq)
    if from_pos < 0:
        rfQ = np.concatenate((np.zeros(-from_pos), rfQ))
        rfT = np.concatenate((np.zeros(-from_pos), rfT))
        to_pos += -from_pos
        from_pos = 0
    if to_pos > len(rfQ):
        rfQ = np.concatenate((rfQ, np.zeros(to_pos - len(rfQ))))
        rfT = np.concatenate((rfT, np.zeros(to_pos - len(rfT))))

    
    stQ.traces[0].data = rfQ[from_pos : to_pos]
    stT.traces[0].data = rfT[from_pos : to_pos]

    stQ.traces[0].stats.starttime = zero_date + time_from
    stT.traces[0].stats.starttime = zero_date + time_from
    
    stQ.traces[0].stats.channel = 'RFQ'
    stT.traces[0].stats.channel = 'RFT'

    data = Stream(stQ.traces + stT.traces)

    # filtering 
    data = data.filter('bandpass', freqmin=filter_config['FREQMIN'], freqmax=filter_config['FREQMAX'])

    # normalization
    if config.NORMALIZE_AFTER:
        mx = max([np.max(t.data) for t in data.traces])
        mn = min([np.min(t.data) for t in data.traces])
        for tr in data.traces:
            tr.data /= mx - mn

    return data


from obspy.core.utcdatetime import UTCDateTime as utc

def _get_zero_date(data):
    if config.TIME0_FORMAT == "zero":
        return utc(0.)
    
    elif config.TIME0_FORMAT == "given":
        return utc(config.TIME0)
    
    elif config.TIME0_FORMAT == "relative":
        return data.traces[0].stats.starttime + config.TIME0_S
    
    else:
        raise NotImplementedError
