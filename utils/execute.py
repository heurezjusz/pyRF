import config
from utils import rotate_theoretical, deconvolve, output_filename
from obspy.core.stream import Stream

def execute_theoretical(data):
    # rotating
    data = rotate_theoretical(data)

    if config.SAVE_ROTATED:
        data.write(output_filename(datafile, prefix='rotated_'), config.SAVE_FORMAT)
    if config.PLOT_ROTATED: data.plot()

    # filtering 
    data = data.filter('bandpass', freqmin=config.FREQMIN, freqmax=config.FREQMAX)

    # normalization
    if config.NORMALIZE:
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

    return Stream(stQ.traces + stT.traces)



def execute_search(data):
    raise NotImplementedError