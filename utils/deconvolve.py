import numpy as np

def deconvolve(signals, function):
    """returns list of deconvolutions of given signals
    using Toeplitz matrix method"""
    
    n = len(function)
    print("n=",n)
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
    r = toeplitz
    g = signal
    a = np.zeros(m)
    b = np.zeros(m)
    f = np.zeros(m)
    
    f[0] = g[0] / r[0]
    a[0] = r[1] / r[0]

    for i in range(1, m):
        gn = r[0]
        z1 = 0. if i == m - 1 else r[i + 1]
        z2 = g[i]

        gn -= np.sum(r[1 : i + 1] * a[0 : i])
        z1 -= np.sum(r[1 : i + 1] * a[0 : i][::-1])
        z2 -= np.sum(r[1 : i + 1] * f[0 : i][::-1])

        a[i] = z1 / gn
        f[i] = z2 / gn
        
        b[0 : i] = a[0 : i] - a[i] * a[0 : i][::-1]
        f[0 : i] -= f[i] * a[0 : i][::-1]
                
        a[ : i] = b[ : i]

    return f



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
