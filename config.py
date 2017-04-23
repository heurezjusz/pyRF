
DELTA = 5.000000e-02
LENGTH = 3601

ARG1 = 195.0
ARG2 = 300.0
ARG3 = 0.1
ARG4 = 1
# ==================================================== #
#                     calculations                     #
# ==================================================== #

# ==================== rotating ======================
# possible mode of rotating.
# "theoretical" calculates inclination angle from theoretical equation
# "search" searches azimuth and inclination angle automatically
ROTATION_MODE = "theoretical"

# %%%%% mode : theoretical
SLOWNESS = 5.523560e+00 / 111.12
DISTANCE = 7.841513e+01
AZIMUTH = 4.339704e+01

# %%%%% mode : search
FIRST_PEAK_POSITION = 148

# normalize data after rotation
NORMALIZE = False

# =================== filtering ======================
# uses ObsPy 'boundpass' filter with parameters FREQMIN and FREQMAX
FREQMIN = 0.03
FREQMAX = 0.8

# ================ receiver function =================
# multiplying Q or T component of receiver function by -1
REVERSE_QRF = True
REVERSE_TRF = False




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
PLOT_DATA_FROM_FILE = True
# plots data after rotation
PLOT_ROTATED = True
# plots calculated receive function
PLOT_RF = True
