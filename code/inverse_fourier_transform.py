import numpy as np

import cmath

import time # Used to calculate the time spent on iDFT

def mirror(FT_need_mirror): # FT_need_mirror is a class 'numpy.ndarray' with dtype=np.complex128
    # The "mirror" function adds a mirror image of a complex conjugate array of the Fourier transform, which was obtained using the "fourier_transform_in_parallel" or "fourier_transform" function.

    mirror_image = FT_need_mirror.copy()
    mirror_image = mirror_image[1:-1]
    mirror_image = np.flip(mirror_image)
    mirror_image = mirror_image.conjugate()
    FT_need_mirror = np.concatenate([FT_need_mirror, mirror_image])
    
    return FT_need_mirror

def inverse_fourier_transform(FT, mirror_image=False):
    
    if mirror_image == True:
        FT = mirror(FT)

    N_FRAMES = FT.size

    iFT = np.zeros(shape=N_FRAMES, dtype=np.complex128) # Declaring an array for the inverse Fourier transform

    to_track_progress = int(N_FRAMES/10)
    progress = 0
    print(f"The beginning of the calculation of the inverse discrete Fourier transform.")
    print(f"iDFT progress: {progress}% \t Iteration: {0}\{N_FRAMES}")
    start_time = time.time() # Starting the stopwatch

    for i in range(N_FRAMES):
        if i == to_track_progress and progress < 90:
                progress +=10
                print(f"iDFT progress: {progress}% \t Iteration: {to_track_progress}\{N_FRAMES}")
                to_track_progress += int(N_FRAMES/10)
        for j in range(N_FRAMES):
            iFT[i] += FT[j] * (cmath.cos((2*cmath.pi*i*j)/N_FRAMES) + 1j*cmath.sin((2*cmath.pi*i*j)/N_FRAMES))
        iFT[i] = iFT[i] * (1/N_FRAMES)

    end_time = time.time() - start_time # Stopping the stopwatch
    print(f"iDFT progress: {100}% \t Iteration: {N_FRAMES}\{N_FRAMES}")
    print(f"The end of the calculation of the inverse discrete Fourier transform. Time spent {'%.3f' % end_time} seconds.\n")

    data_signal = np.around(iFT.real)
    data_signal = data_signal.astype(np.int32)

    return (iFT, data_signal)

if __name__ == "__main__":
    test = np.array([(-6+0j), (-175.88932753224321-1056.7982764394924j),
                     (-1064.2060633617727-86.44860954814493j),
                     (-116.9430893764694+171.07090293453746j),
                     (-7.370251172379312+212.28830044671426j),
                     (662-0j)], dtype=np.complex128)
    
    inverse_fourier_transform(test, True)
