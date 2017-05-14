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
# set "zero moment" (theoretical beggining of the event)
# RF_SHIFT seconds after events' window
RF_SHIFT = 1.


# =================== filtering ======================
# uses ObsPy 'boundpass' filter with parameters FREQMIN and FREQMAX
FILTER_FREQ = {'FREQMIN': 0.03, 'FREQMAX': 0.8}


# ==================================================== #
#                       rotating                       #
# ==================================================== #
# possible mode of rotaion.
# "theoretical" calculates azimuth and inclination angles from theoretical equations
# "search" searches azimuth and inclination angle automatically
MODE = "theoretical"
#MODE = "search"

# verbosity level - level of details printed by program
VERBOSITY = 3


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
SEARCH_FILTER_FREQ = {'FREQMIN': 0.1, 'FREQMAX': 0.5}


# ---------------------------------------------------- #
#               theoretical mode options               #
# ---------------------------------------------------- #

SLOWNESS = 5.523560e+00 / 111.12
DISTANCE = 7.841513e+01
AZIMUTH = 4.339704e+01
#AZIMUTH = 31


# ==================================================== #
#                    saving results                    #
# ==================================================== #
# format of data to be saved (in ObsPy convention)
SAVE_FORMAT = "MSEED"
# save data after rotation, filename: rotated_[filename]
SAVE_ROTATED = False
# save calculated receive function, filename: rf_[filename]
SAVE_RF = True


# ==================================================== #
#                   plotting results                   #
# ==================================================== #
# plots data from readed file
PLOT_DATA_FROM_FILE = False
# plots data after rotation
PLOT_ROTATED = False
# plots calculated receive function
PLOT_RF = True
