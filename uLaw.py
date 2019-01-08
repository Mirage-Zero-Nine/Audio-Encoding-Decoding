__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: uLaw
Create Time: 11/20/18 21:58
'''

import numpy as np
import math
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S'
                    )


def u_law_compress(arr):
    """
    u-Law compress function
    :param arr: given array
    :return: compressed array
    """
    max_in_arr = np.amax(arr)
    u = 255
    out = np.array(arr, dtype=float)
    de = math.log(1 + u)
    for i in range(0, len(arr)):

        up = 1 + u * abs(arr[i])
        o = (math.log(up) * max_in_arr) / de
        if arr[i] < 0:
            o = -o
        out[i] = o

    return out


def u_law_expend(arr):
    """
    Expend compressed array.
    :param arr: given array
    :return: expended array
    """
    u = 255
    max_in_arr = np.amax(arr)

    out = np.array(arr, dtype=float)
    for i in range(0, len(arr)):

        p = math.log(256) * abs(arr[i]) / max_in_arr
        o = max_in_arr * (math.exp(p) - 1) / u
        if arr[i] < 0:
            o = -o
        out[i] = o

    return out


if __name__ == '__main__':
    # print(math.log(1 + 255))
    # array = [0.01, 0.02]
    # print(array)
    # print(u_law_compress(array))
    pass
