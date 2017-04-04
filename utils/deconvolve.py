import numpy as np

def deconvolve(signals, function):
    """returns list of deconvolutions of given signals
    using Toeplitz matrix method"""
    
    n = len(function)
    print("n=",n)
   # print("creating matrix")
   # c = np.asarray(function)
   # 
   # toeplitz = np.zeros((n,n))
   # for i in range(0, n):
   #     for j in range(0, n):
   #         toeplitz[i][j] = function[(i - j + n) % n]
   # print(toeplitz)

   # print("inverting...")
   # toeplitz_inv = np.linalg.inv(toeplitz)
   # print(toeplitz_inv)
    
   # print("counting result...")
   # spikes = [spikefil(s) for s in signals]
   # fun = spikefil(function)
   # return [s / fun for s in spikes]

    fff = np.fft.fft(function)
    ffs = [np.fft.fft(s) / fff for s in signals]
    return [np.fft.ifft(fs) for fs in ffs]


def levinson(toeplitz, signal):
    """
    input:
    toeplitz: 1D numpy.array coding toeplitz matrix
    signal: b

    returns: solution of equation T * x = b
    """
    # todo: input checking
    m = len(toeplitz)
    r = np.insert(toeplitz, 0, 0)
    g = np.insert(signal, 0, 0)
    a = np.zeros(m + 1)
    b = np.zeros(m + 1)
    f = np.zeros(m + 1)
    
    f[1] = g[1] / r[1]
    a[1] = r[2] / r[1]

    for i in range(2, m+1):
        gn = r[1]
        z1 = 0. if i == m else r[i + 1]
        z2 = g[i]

        for j in range(2, i+1):
            gn -= r[j] * a[j-1]
            z1 -= r[j] * a[i-j+1]
            z2 -= r[j] * f[i-j+1]

        a[i] = z1 / gn
        f[i] = z2 / gn
        
        for j in range(1, i):
            b[j] = a[j] - a[i] * a[i - j]
            f[j] -= f[i] * a[i - j]
        
        for j in range(1, i):
            a[j] = b[j]

    return f[:-1]



from scipy.signal import wiener
def spikefil(trc):
    return wiener(trc)
    trclth = len(trc)
    t0 = 0 # some t0 on max
    tmp = trc[0]
    for i in range(1, trclth):
        if abs(trc[i]) > tmp:
            tmp, t0 = trc[i], i
    ac = np.zeros(trclth)
    ccr = np.zeros(trclth)
    for d in range(0, trclth):
        for i in range(d, trclth):
            ac[d] += trc[i] * trc[i - d]

    reg = 0
    ac[0] *= 1. + reg

    for i in range(0, t0+1):
        ccr[i] += trc[t0-i]
    for i in range(t0+1, trclth):
        ccr[i] = 0
    return levinson(ac, ccr)
