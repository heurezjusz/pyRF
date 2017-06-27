# pyRF
Program to calculate receiver function from seismology data 

Usage:
./calcrf
or
./calcrf DATAFOLDER

In first case DATAFOLDER should be defined in config.py
DATAFOLDER should contain DATAFILES in following format:
* every DATAFILE should contain one stream of one event registered by one station
* DATAFILE should be named [station_name]_[event_id], where event_id is event date in format YYMMDD_hhmmss,
    for example KSP_070716_011322.mseed
