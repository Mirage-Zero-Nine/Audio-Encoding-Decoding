__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: ADPCM
Create Time: 11/20/18 22:40
'''
import numpy as np
import logging

IndexTable = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]
StepSizeTable = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80,
                 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598,
                 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327,
                 3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 15289,
                 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767]


def encoder(raw_y):
    out = np.array(raw_y, dtype=int)

    previous_sample = 0
    previous_index = 0
    length = len(raw_y)
    n = 0

    while n < length:
        predict_sample = previous_sample
        index = previous_index
        step = StepSizeTable[index]
        diff = raw_y[n] - predict_sample

        if diff >= 0:
            code = 0
        else:
            code = 8
            diff = -diff

        temp_step = step

        if diff >= temp_step:
            code = code | 4  # OR operation
            diff = diff - temp_step

        temp_step = temp_step >> 1  # Shift right 1 bit

        if diff >= temp_step:
            code = code | 2
            diff = diff - temp_step

        temp_step = temp_step >> 1

        if diff >= temp_step:
            code = code | 1

        different_quantized = step >> 3

        if code & 4:
            different_quantized = different_quantized + step

        if code & 2:
            different_quantized = different_quantized + step >> 1

        if code & 1:
            different_quantized = different_quantized + step >> 2

        if code & 8:
            predict_sample = predict_sample - different_quantized
        else:
            predict_sample = predict_sample + different_quantized

        if predict_sample > 32767:
            predict_sample = 32767
        elif predict_sample < -32768:
            predict_sample = -32768

        index = index + IndexTable[code]

        if index < 1:
            index = 1
        if index > 89:
            index = 89

        previous_sample = predict_sample
        previous_index = index

        out[n] = code & 15

        n += 1

    return out


def decoder(adpcm_y):
    out = np.array(adpcm_y, dtype=int)

    previous_sample = 0
    previous_index = 0

    length = len(adpcm_y)
    n = 0

    while n < length:
        predict_sample = previous_sample
        index = previous_index
        step = StepSizeTable[index]
        code = adpcm_y[n]

        different_quantized = step >> 3

        if code & 4:
            different_quantized = different_quantized + step
        if code & 2:
            different_quantized = different_quantized + step >> 1
        if code & 1:
            different_quantized = different_quantized + step >> 2
        if code & 8:
            predict_sample = predict_sample - different_quantized
        else:
            predict_sample = predict_sample + different_quantized

        if predict_sample > 32767:
            predict_sample = 32767
        elif predict_sample < -32768:
            predict_sample = -32768

        index = index + IndexTable[code]

        if index < 1:
            index = 1
        if index > 89:
            index = 89

        previous_sample = predict_sample
        previous_index = index

        # print(predict_sample)

        # out[n] = predict_sample / 32767
        out[n] = predict_sample
        n += 1

    return out


if __name__ == '__main__':
    pass
