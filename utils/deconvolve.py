import numpy as np

def deconvolve(signals, function):
    """returns list of deconvolutions of given signals
    using Toeplitz matrix method"""
    
    n = len(function)
    print("n=",n)
    print("creating matrix")
    toeplitz = np.zeros((n,n))
    for i in range(0, n):
        for j in range(0, n):
            toeplitz[i][j] = function[(i - j + n) % n]

    print("inverting...")
    toeplitz_inv = np.linalg.inv(toeplitz)
    
    print("counting result...")
    return [np.dot(s, toeplitz_inv) for s in signals]
