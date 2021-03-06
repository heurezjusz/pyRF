# verbosity level - level of details printed by program
VERBOSITY = 0

DATAFOLDER = 'example/data'


# create file with logs - for every datafile
#   prints recognized event, station code and OK or ERROR
#   in case of error during computations.
#   After an error datafile is skipped.
# filename: out/logs_[date].txt
LOGS = True

# create file with error details - in case of error
#   prints datafile, recognized station end event and full traceback
#   for every error during computations. After an error datafile is skipped.
# filename: out/err_details_[date].txt
ERROR_DETAILS = True

# ==================================================== #
#                  receiver function                   #
# ==================================================== #
# normalize data before and after deconvolution
NORMALIZE_BEFORE = False
NORMALIZE_AFTER = False

# multiplying Q or T component of receiver function by -1
REVERSE_QRF = True
REVERSE_TRF = False

# =================== time window ======================
# *** DATA
# Cutting events' time window from datafile. Possible modes:
#  "none" - do not cut. All data from file are used to calculations
#  "dates" - use data between START_DATE and END_DATE.
#            START_DATE and END_DATE should be provided in "RRRR-MM-DDThh:mm:ss.(miliseconds) format
#            (example below)
#  "date_len" - use WINDOW_LEN (float) seconds beggining at START_DATE.
#  "seconds" - use data between START_SECOND and END_SECOND (float).
#              Seconds are counted from begginig of the file.

CUT_MODE = "none"

#CUT_MODE = "dates"
#START_DATE = "2007-07-16T01:25:17.9"
#END_DATE = "2007-07-16T01:27:02.97"

#CUT_MODE = "date_len"
#START_DATE = "2007-07-16T01:25:17.9"
#WINDOW_LEN = 105.

#CUT_MODE = "seconds"
#START_SECOND = 10 * 60 - 5
#END_SECOND = 10 * 60 + 195

# ==== RESULT time window ====
# Result time frame measured from time 0.
# obtained receival function will be cutted to time frame below (in seconds, float):
RF_TIME_FROM = -5.
RF_TIME_TO = 30.


# =================== time 0 output format ======================
# set time 0 as 0s (obspy interpretes 0s as 00:00 of 01.01.1970)
TIME0_FORMAT = "zero"

# set time 0 as given date.
# Date should be provided in "RRRR-MM-DDThh:mm:ss.(miliseconds) format (example below)
#TIME0_FORMAT = "given"
#TIME0 = "2007-07-16T01:25:17.9"

# set time 0 TIME0_S (float) seconds after beginning of time window
#     (see 'time window' section above)
#TIME0_FORMAT = "relative"
#TIME0_S = 0.


# time 0 will be set RF_SHIFT seconds after the theoretical time 0 (maximum in deconvolved L trace)
RF_SHIFT = 0.


# =================== filtering ======================
# uses ObsPy 'boundpass' filter with parameters FREQMIN and FREQMAX
FILTER_FREQ = { 'FREQMIN': 0.03, 'FREQMAX': 0.8 }


# ==================================================== #
#                       rotating                       #
# ==================================================== #
# possible mode of rotaion.
# "theoretical" calculates azimuth and inclination angles from theoretical equations
# "search" searches azimuth and inclination angle automatically
MODE = "theoretical"
#MODE = "search"


# ---------------------------------------------------- #
#                   search mode options                #
# ---------------------------------------------------- #

# minimum and maximum angle of azimuth and inclination
# grid search algorithm will iterate through angles between
# 'min' and 'max' with given 'step'
AZIMUTH_ANGLES = { 'min': 0., 'max': 359, 'step': 1 }
INCLINATION_ANGLES = { 'min': 0., 'max': 45., 'step': 0.5 }

# =================== filtering ======================
# parameters FREQMIN and FREQMAX for ObsPy 'boundpass' filter
# used during angles searching
SEARCH_FILTER_FREQ = { 'FREQMIN': 0.1, 'FREQMAX': 0.5 }


# ---------------------------------------------------- #
#              theoretical mode constants              #
# ---------------------------------------------------- #
# earth radius in meters
EARTH_RADIUS = 6378137.0

# ===== average velocity of S-waves in shell =====
# velocity for station in format ('station ID': velocity in km/s)
VS_STATION = {
    'KSP': 1.3,
}
# velocity for stations not mentioned in VS_STATION
import math
VS_DEFAULT = 6. / math.sqrt(3)


# ==== slowness and back-azimuth of the event ====
#  It is possible to pass SLOWNESS and AZIMUTH constants manually
#  (COLLECTDATA_MODE = "manual"), but it can be counted automatically
#  from events and stations data (COLLECTDATA_MODE = "find")

# --- passing the constants manually
#COLLECTDATA_MODE = "manual"
#SLOWNESS = 5.523560e+00 / 111.12
#AZIMUTH = 4.339704e+01

# --- counting the values from station and event's data:
COLLECTDATA_MODE = 'find'

# File with stations data.
# program supports file format from * database
# (see example/stationlist.txt)
STATIONS_DATA = 'example/stationlist.txt'

# File with events data.
# Program supports two most popular formats:
# european (EVENTS_FORMAT = "EU", file: example/eventlist_eu.txt) and american
#EVENTS_FORMAT = 'EU'
#EVENTS_DATA = 'example/eventlist_eu.txt'

EVENTS_FORMAT = 'US'
EVENTS_DATA = 'example/eventlist_us.csv'


# ==================================================== #
#                    saving results                    #
# ==================================================== #
# Azimuth and inclination angles will be calculated in both,
# theoretical and search ways. Results will be stored in out/angles_[date].txt
# To calculate final receival function will be used angles chosen by 'MODE' method.
COMPARE_ANGLES = False

# ==================================================== #
#                    saving results                    #
# ==================================================== #
# format of data to be saved (in ObsPy convention)
SAVE_FORMAT = "SAC"
# save data after cutting, filename: cut_[filename]
SAVE_CUT = False
# save data after rotation, filename: rotated_[filename]
SAVE_ROTATED = True
# save calculated receive function, filename: rf_[filename]
SAVE_RF = True


# ==================================================== #
#                   plotting results                   #
# ==================================================== #
# plots data from readed file
PLOT_DATA_FROM_FILE = False
# plot data after cutting, filename: cut_[filename]
PLOT_CUT = False
# plots data after rotation
PLOT_ROTATED = False
# plots calculated receive function
PLOT_RF = True


PLOT_FILE_CUT = True
PLOT_FILE_ROTATED = True
PLOT_FILE_RF = True
