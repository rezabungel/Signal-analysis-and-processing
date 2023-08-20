'''
This module is used to calculate the inverse discrete Fourier transform and obtain signal data.
The inverse discrete Fourier transform is computed using the inverse fast Fourier Transform algorithm. (note: For "ifft" the amount of data must be a power of two.)
The inverse discrete Fourier transform is calculated from the data of the discrete Fourier transform. Signal data is the value of the signal in time.
'''

import numpy as np

import cmath

import time # Used to calculate the time spent on iFFT

import isPowerOfTwo

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def ifft(FT):
    
    '''
    This function is used to calculate the inverse discrete Fourier transform using the inverse fast Fourier Transform algorithm. (note: It is used for "inverse_fast_fourier_transform" but can also be used independently.)
    The following parameters are passed to the function:
        FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform (note: The amount of data must be a power of two.).
    The result of the function:
        Return values:
            iFT ("numpy.ndarray" with dtype="numpy.complex128") - values of the inverse discrete Fourier transform
            or
            -1 ("int") - if the amount of data is not a power of two.
    '''

    def iFFT(FT):
        n = len(FT) # n is a power of 2
        if n == 1:
            return FT
        omega = (cmath.cos(2*cmath.pi/n) + 1j*cmath.sin(2*cmath.pi/n))
        FT_even, FT_odd = FT[::2], FT[1::2]
        y_even, y_odd = iFFT(FT_even), iFFT(FT_odd)
        iFT = np.zeros(shape=n, dtype=np.complex128)
        for i in range(int(n/2)):
            iFT[i] = y_even[i]+(omega**i)*y_odd[i]
            iFT[i+int(n/2)] = y_even[i]-(omega**i)*y_odd[i]
        return iFT

    # Checking that the amount of data corresponds to a power of two.
    if not isPowerOfTwo.isPowerOfTwo(len(FT)):
        print(f'The amount of data does not correspond to a power of two (the "ifft" function cannot be used).')
        print(f"The function terminates with a return of -1.")
        return -1

    iFT = iFFT(FT)
    iFT = iFT * (1/len(iFT))
    return iFT

def mirror(FT_need_mirror):
    
    '''
    The "mirror" function adds a mirror image of a complex conjugate array of the Fourier transform, which was obtained using the "fast_fourier_transform", "fourier_transform_in_parallel" or "fourier_transform" function.
    The following parameters are passed to the function:
        FT_need_mirror ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform. (note: elements from the first to the penultimate will be mirrored and complex conjugate).
    The result of the function:
        Return values:
            FT_need_mirror ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform with added mirror imaged complex conjugate values of the discrete Fourier transform.
    '''

    mirror_image = FT_need_mirror.copy()
    mirror_image = mirror_image[1:-1]
    mirror_image = np.flip(mirror_image)
    mirror_image = mirror_image.conjugate()
    FT_need_mirror = np.concatenate([FT_need_mirror, mirror_image])

    return FT_need_mirror

def inverse_fast_fourier_transform(FT, mirror_image=False):
    
    '''    
    This function allows you to calculate the inverse discrete Fourier transform (using the inverse fast Fourier transform algorithm (function "ifft")) and the value of the signal data.
    The following parameters are passed to the function:
        FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform. (note: The amount of data must be a power of two.);
        mirror_image ("bool") - If "True", the "mirror" function will be called, if "False", the "mirror" function will not be called.
    The result of the function:
        Return values:
            iFT ("numpy.ndarray" with dtype="numpy.complex128") - values of the inverse discrete Fourier transform;
            data_signal ("numpy.ndarray" with dtype="numpy.int32") - value of the signal data
            or
            -1 ("int") - if the amount of data is not a power of two
            or
            -2 ("int") - if an error occurs in the values of the discrete Fourier transform, incorrect data is provided, instead of the expected "numpy.ndarray" with dtype="numpy.complex128".
    '''

    # Checking for the correctness of the input data
    if type(FT) != np.ndarray or FT.dtype != np.complex128:
        print(f'Error in the values of the discrete Fourier transform. Was expected "numpy.ndarray" with dtype="numpy.complex128".')
        print(f"The function terminates with a return of -2.")
        return -2

    if type(mirror_image) != bool:
        mirror_image = False
        print(f'The boolean key value "mirror_image" is specified incorrectly. The default value is set:\n\t mirror_image = "{mirror_image}"')

    if mirror_image == True:
        FT = mirror(FT)

    print(f"The beginning of the calculation of the inverse fast Fourier transform.")
    print(f"iFFT progress...")
    start_time = time.time() # Starting the stopwatch

    iFT = ifft(FT)

    if type(iFT) == int:
        return -1

    end_time = time.time() - start_time # Stopping the stopwatch
    print(f"The end of the calculation of the inverse fast Fourier transform. Time spent {'%.3f' % end_time} seconds.\n")

    data_signal = np.around(iFT.real)
    data_signal = data_signal.astype(np.int32)
    data_signal = data_signal

    return (iFT, data_signal)

if __name__ == "__main__":
    test = np.array([(-6+0j), (-175.88932753224321-1056.7982764394924j),
                     (-1064.2060633617727-86.44860954814493j),
                     (-116.9430893764694+171.07090293453746j),
                     (-7.370251172379312+212.28830044671426j),
                     (54.540300602228434-389.30826936699845j),
                     (-51.8776736059967-38.42405107224924j),
                     (-103.7553472119934-76.84810214449848j),
                     (662-0j)], dtype=np.complex128)

    inverse_fast_fourier_transform(test, True) # The length of "test" is 9, but inside the "inverse_fast_fourier_transform" function, the "mirror" function will be called (since the "True" flag was passed), resulting in the array size becoming 16 (which is a power of two, as required for the inverse fast Fourier transform algorithm).
