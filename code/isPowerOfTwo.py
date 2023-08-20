'''
This module is used to check if a number is a power of two.
'''

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

if __name__ == "__main__":
    num = -1
    while num <= 0:
        num = int(input("Enter a number > 0 to check if it is a power of two. "))
    print(isPowerOfTwo(num))
