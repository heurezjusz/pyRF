import numpy as np

def deconvolve(signals, function):
    """returns list of deconvolutions of given signals
    using Toeplitz matrix method"""
    
    n = len(function)
    print("n=",n)
    print("creating matrix")
    c = np.asarray(function)
   # 
   # toeplitz = np.zeros((n,n))
   # for i in range(0, n):
   #     for j in range(0, n):
   #         toeplitz[i][j] = function[(i - j + n) % n]
   # print(toeplitz)

   # print("inverting...")
   # toeplitz_inv = np.linalg.inv(toeplitz)
   # print(toeplitz_inv)
    
    print("counting result...")
    return [levinson(c, s) for s in signals]



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
