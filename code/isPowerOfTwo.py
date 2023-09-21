'''
This module is used to check if a number is a power of two.
'''

import cmath
import math

def isPowerOfTwo(num):

    '''
    This function is used to check if a number is a power of two.
    The following parameters are passed to the function:
        num ("int" and greater than 0) - a value being examined to determine if it is a power of two.
    The result of the function:
        Return values:
            True ("bool") - if the number is a power of two
            or
            False ("bool") - if the number is not a power of two.
    '''

    if num & (num - 1) == 0 and num > 0:
        return True
    else:
        return False

def isPowerOfTwo_DataVolume(seconds, rate, chunk):

    '''
    This function is used to ...
    '''

    # Checking if the volume of recorded data matches a power of two. (If it doesn't match, it can be corrected by changing the recording duration.)
    len_data_signal = int(rate / chunk * seconds)*chunk # It is possible to use only 'int(rate / chunk * seconds)' since chunk is a power of two
    if not isPowerOfTwo(len_data_signal):
        print(f'The recorded data volume will not match a power of two (the "fft" function will not be usable).')
        while True:
            try:
                while True:
                    answer = int(input('To use the "fft" function, you will have to change the recording duration. Do you want to do this (1/0)?\t'))
                    if answer == 0 or answer == 1:
                        break
                    else:
                        print(f"Invalid input. Non-existent answer.")
                break
            except ValueError:
                print(f"Invalid input. You didn't enter a number.")

        if answer == 0:
            return seconds

        else:
            temp = cmath.log(int(rate / chunk * seconds), 2).real
            hint = [.0, .0]
            
            hint[0] = (2**float(int(temp))) / (rate / chunk)
            hint[1] = (2**float(int(temp+1))) / (rate / chunk)

            hint[0] = math.ceil(hint[0]*100)/100
            hint[1] = math.ceil(hint[1]*100)/100

            while True:
                try:
                    while True:
                        answer = int(input(f'Choose the recording duration: \n0: {hint[0]} \n1: {hint[1]} \nAnswer... '))
                        if answer == 0 or answer == 1:
                            break
                        else:
                            print(f"Invalid input. Non-existent answer.")
                    break
                except ValueError:
                    print(f"Invalid input. You didn't enter a number.")

            print(f'Now the recorded data volume will correspond to a power of two (the "fft" function will be usable).')
            seconds = hint[answer]
            return seconds
    else:
        print(f'The recorded data volume will correspond to a power of two (the "fft" function will be usable).')
        return seconds

if __name__ == "__main__":
    num = -1
    while num <= 0:
        num = int(input("Enter a number > 0 to check if it is a power of two. "))
    print(f'{isPowerOfTwo(num)}\n')

    seconds = 1.0
    rate = 44100
    chunk = 1024
    seconds = isPowerOfTwo_DataVolume(seconds, rate, chunk)
