'''
This module is used to calculate the inverse discrete Fourier transform and obtain signal data.
The calculation of the inverse discrete Fourier transform is parallelized into 8 cores. If there are fewer or more cores, this will not cause problems.
The inverse discrete Fourier transform is calculated from the data of the discrete Fourier transform. Signal data is the value of the signal in time.
'''

import numpy as np

import multiprocessing

import cmath

import time # Used to calculate the time spent on iDFT

def iDFT(index_start, index_stop, N_FRAMES, FT):

    '''
    This function is used to calculate the inverse discrete Fourier transform when parallelizing calculations. (note: This function is used in conjunction with the "inverse_fourier_transform_in_parallel" function. The "iDFT" function is not used separately.)
    The following parameters are passed to the function:
        index_start (dtype="numpy.uint32") - index of the beginning of the calculation; 
        index_stop (dtype="numpy.uint32") - index of the end of the calculation;
        N_FRAMES ("int") - the number of frames;
        FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform.
    The result of the function:
        Return values:
            iFT ("numpy.ndarray" with dtype="numpy.complex128") - values of the inverse discrete Fourier transform (from index_start to the index_stop).
    '''

    # inverse Discrete Fourier transform (iDFT)
    iFT = np.zeros(shape=N_FRAMES, dtype=np.complex128)

    for i in range(index_start, index_stop):
        precomp = 2*cmath.pi*i/N_FRAMES
        iFT[i] = sum(FT[j] * (cmath.cos(precomp*j) + 1j*cmath.sin(precomp*j)) for j in range(N_FRAMES))
        iFT[i] = iFT[i] * (1/N_FRAMES)
    else:
        print(f"iDFT progress: +{12.5}% \t Iteration: {'%6d' % index_start} -> {'%6d' % i}\{N_FRAMES} completed.")

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

def inverse_fourier_transform_in_parallel(FT, mirror_image=False):
    
    '''
    This function allows you to calculate the inverse discrete Fourier transform (parallelizing calculations by 8 cores) and the value of the signal data.
    The following parameters are passed to the function:
        FT ("numpy.ndarray" with dtype="numpy.complex128") - values of the discrete Fourier transform;
        mirror_image ("bool") - If "True", the "mirror" function will be called, if "False", the "mirror" function will not be called.
    The result of the function:
        Return values:
            iFT ("numpy.ndarray" with dtype="numpy.complex128") - values of the inverse discrete Fourier transform;
            data_signal ("numpy.ndarray" with dtype="numpy.int32") - value of the signal data.
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

    N_FRAMES = FT.size

    iFT = np.zeros(shape=N_FRAMES, dtype=np.complex128) # Declaring an array for the inverse Fourier transform

    print(f"The beginning of the calculation of the inverse discrete Fourier transform.")
    print(f"iDFT progress: {0}% \t Iteration: {0}\{N_FRAMES}")
    start_time = time.time() # Starting the stopwatch

    # Creating calculation intervals for each core
    step = int(N_FRAMES/8)
    interval = np.zeros(9, dtype=np.uint32)
    interval[0] = 0
    for i in range(1, 8):
        interval[i] = interval[i-1] + step
    interval[8] = N_FRAMES

    # Parallelization of iDFT calculation on 8 cores. (If there are fewer or more cores, this is not a problem)
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        temp = p.starmap(iDFT, [(interval[0], interval[1], N_FRAMES, FT),
                                (interval[1], interval[2], N_FRAMES, FT),
                                (interval[2], interval[3], N_FRAMES, FT),
                                (interval[3], interval[4], N_FRAMES, FT),
                                (interval[4], interval[5], N_FRAMES, FT),
                                (interval[5], interval[6], N_FRAMES, FT),
                                (interval[6], interval[7], N_FRAMES, FT),
                                (interval[7], interval[8], N_FRAMES, FT)])

    # Assembling data from a parallel computation into a single data array
    for i in range(len(interval)-1):
        for j in range(interval[i], interval[i+1]):
            iFT[j]=temp[i][j]

    end_time = time.time() - start_time # Stopping the stopwatch
    print(f"iDFT progress: {100}% \t Iteration: {N_FRAMES}\{N_FRAMES}")
    print(f"The end of the calculation of the inverse discrete Fourier transform. Time spent {'%.3f' % end_time} seconds.\n")

    data_signal = np.around(iFT.real)
    data_signal = data_signal.astype(np.int32)

    return (iFT, data_signal)

if __name__ == "__main__":
    multiprocessing.freeze_support() # Enable support for multiprocessing
    test = np.array([(-6+0j), (-175.88932753224321-1056.7982764394924j),
                     (-1064.2060633617727-86.44860954814493j),
                     (-116.9430893764694+171.07090293453746j),
                     (-7.370251172379312+212.28830044671426j),
                     (54.540300602228434-389.30826936699845j),
                     (-51.8776736059967-38.42405107224924j),
                     (662-0j)], dtype=np.complex128)

    inverse_fourier_transform_in_parallel(test, True)
