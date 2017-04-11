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
    

    # fff = np.fft.rfft(function)
    # ffs = [np.fft.rfft(s) / fff for s in signals]
    # return [np.fft.irfft(fs) for fs in ffs]

    print("counting filter")
    filt = spikefil(function, type="center")
    print("counting result")
    return [np.convolve(s, filt) for s in signals]


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

        gn -= np.sum(r[2 : i + 1] * a[1 : i])
        z1 -= np.sum(r[2 : i + 1] * a[1 : i][::-1])
        z2 -= np.sum(r[2 : i + 1] * f[1 : i][::-1])

        a[i] = z1 / gn
        f[i] = z2 / gn
        
        b[1 : i] = a[1 : i] - a[i] * a[1 : i][::-1]
        f[1 : i] -= f[i] * a[1 : i][::-1]
                
        a[ : i] = b[ : i]

    return f[:-1]



from scipy.signal import wiener
def spikefil(trc, type="max", spike_pos=None):
    trclth = len(trc)
    t0 = 0 # spike position

    if type not in [ "max", "beginning", "end", "center", "given", "mass_center" ]:
        raise NotImplementedError
    if type == "max":
        t0 = np.argmax(trc)
    if type == "beginning":
        t0 = 0
    if type == "end":
        t0 = trclth - 1
    if type == "center":
        t0 = trclth // 2
    if type == "given":
        if spike_pos is None:
            raise RuntimeError("spikefil: in mode \'given\' spike_pos should be specified")
        t0 = spike_pos
    if type == "mass_center":
        a = np.asarray(range(0, trclth))
        t0 = int(np.sum(np.abs(trc * a)) / np.sum(np.abs(trc)))

    print("t0=", t0)

    ac = np.zeros(trclth)
    ccr = np.zeros(trclth)
    for d in range(0, trclth):
        ac[d] = np.sum(trc[d:] * trc[: trclth - d])

    reg = 0
    ac[0] *= 1. + reg

    ccr[:t0 + 1] = trc[:t0 + 1][::-1]
    
    print("levinson...\n")
    return levinson(ac, ccr)
