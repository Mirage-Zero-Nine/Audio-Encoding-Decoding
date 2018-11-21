__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: Quantization
Create Time: 11/21/18 09:33
'''

import math
import numpy as np


def quantization(arr, max, type='float'):
    """

    :param arr: input array
    :param max: max int for quantization
    :param type: output array type
    :return: quantizated array
    """
    if type == 'float':
        out = np.array(arr, dtype=float)
    elif type == 'int':
        out = np.array(arr, dtype=int)
    else:
        raise TypeError("Wrong output format!")

    for i in range(0, len(arr)):
        o = arr[i] / max
        if o > 1:
            o = 1
        elif o < -1:
            o = -1
        out[i] = o

    return out


def inverse_quantization(arr, max, type='int'):
    """

    :param arr: input array
    :param max: max int for quantization
    :param type: output array type
    :return: quantizated array
    """
    if type == 'float':
        out = np.array(arr, dtype=float)
    elif type == 'int':
        out = np.array(arr, dtype=int)
    else:
        raise TypeError("Wrong output format!")

    for i in range(0, len(arr)):

        o = arr[i] * max
        if o > max:
            o = max
        elif o < -max:
            o = -max
        out[i] = o

    return out


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    in_list = np.array(arr, dtype=int)
    a = quantization(in_list, np.amax(in_list))
    b = inverse_quantization(a, 5)
    print(a)
    print(b)
