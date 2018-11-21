__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: uLaw
Create Time: 11/20/18 21:58
'''

import numpy as np
import math


def u_law_compress(arr):
    max_in_arr = np.amax(arr)
    u = 255
    out = np.array(arr, dtype=float)
    de = math.log(1 + u)
    for i in range(0, len(arr)):

        up = 1 + u * abs(arr[i])
        # print(up)
        o = (math.log(up) * max_in_arr) / de
        if arr[i] < 0:
            o = -o
        out[i] = o

    return out


def u_law_expend(arr, max_in_arr):
    u = 255
    max_in_arr = np.amax(arr)

    out = np.array(arr, dtype=float)
    for i in range(0, len(arr)):

        # if arr[i] > 0:
        #     sign = True
        # else:
        #     sign = False

        p = math.log(256) * abs(arr[i]) / max_in_arr
        # if not sign:
        #     p = -p
        o = max_in_arr * (math.exp(p) - 1) / u
        # print(o)
        if arr[i] < 0:
            o = -o
        out[i] = o

    return out


if __name__ == '__main__':
    # print(math.log(1 + 255))
    arr = [0.01, 0.02]
    print(arr)
    print(u_law_compress(arr))
