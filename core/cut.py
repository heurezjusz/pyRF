import config
from obspy.core.utcdatetime import UTCDateTime

def cut(data):
    if config.CUT_MODE == "none":
        return data

    if config.CUT_MODE == "dates":
        startdate = UTCDateTime(config.START_DATE)
        enddate = UTCDateTime(config.END_DATE)
        return data.slice(startdate, enddate)

    if config.CUT_MODE == "date_len":
        startdate = UTCDateTime(config.START_DATE)
        return data.slice(startdate, startdate + config.WINDOW_LEN)
    
    if config.CUT_MODE == "seconds":
        startdate = data.traces[0].stats['starttime']
        return data.slice(startdate + config.START_SECOND, startdate + config.END_SECOND)
