import numpy as np

import cmath

import time # Used to calculate the time spent on iDFT

def mirror(FT_need_mirror): # FT_need_mirror is a class 'numpy.ndarray' with dtype=np.complex128
    # The "mirror" function adds a mirror image of the Fourier transform array that was obtained using the "fourier_transform_in_parallel" or "fourier_transform" function.

    mirror_image = FT_need_mirror.copy()
    mirror_image = mirror_image[1:-1]
    mirror_image = np.flip(mirror_image)
    FT_need_mirror = np.concatenate([FT_need_mirror, mirror_image])

    return FT_need_mirror

def inverse_fourier_transform(FT, mirror_image=False):
    
    if mirror_image == True:
        FT = mirror(FT)

    pass

if __name__ == "__main__":
    test = np.array([(-6+0j), (-175.88932753224321-1056.7982764394924j),
                     (-1064.2060633617727-86.44860954814493j),
                     (-116.9430893764694+171.07090293453746j),
                     (-7.370251172379312+212.28830044671426j),
                     (662-0j)], dtype=np.complex128)
    
                    # (-7.370251172379312-212.28830044671426j)	212.41620255738115
                    # (-116.9430893764694-171.07090293453746j)	207.2219582567225
                    # (-1064.2060633617727+86.44860954814493j)	1067.7115281707738
                    # (-175.88932753224321+1056.7982764394924j)	1071.335452892896

    inverse_fourier_transform(test, True)
