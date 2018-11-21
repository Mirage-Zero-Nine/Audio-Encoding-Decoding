__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: uLaw
Create Time: 11/20/18 21:58
'''

import numpy as np
import math


def u_law_encode(vector, max=32768):
    u = 255
    out = np.array(vector, dtype=float)
    de = math.log(1 + u)
    for i in range(0, len(vector)):
        # print("vector[i] = " + str(vector[i]))
        if vector[i] >= 0:
            sign = 1
        else:
            sign = -1
        # print("abs(vector[i] / max) = " + str(abs(vector[i] / max)))

        # up = math.log(1 + u * abs(vector[i] / max))

        out[i] = sign * (math.log(1 + u * abs(vector[i] / max)) / de)

        # print(abs(vector[i] / max))
    # print(out)
    return out


def u_law_decode(vector, max=128):
    u = 256

    out = vector.astype(float)
    # normalized_signal = (out / u - 0.5) * 2.0

    # inv mu-law
    mu = u - 1
    # signals_1d = np.sign(normalized_signal) * ((1 + mu) ** np.absolute(normalized_signal)) / mu
    for i in range(0, len(vector)):
        if vector[i] >= 0:
            sign = 1
        else:
            sign = -1
        out[i] = sign * (pow((1 + u), abs(vector[i]) - 1) / u)
        out[i] *= max

    # print(out)
    # signals_1d *= max
    # print(signals_1d)
    return out
