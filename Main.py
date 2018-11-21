__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: Main.py
Create Time: 11/20/18 11:34
'''

from scipy.io.wavfile import read
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import math
import audioop
import os
import wave
import Encoder
import Decoder
import uLaw
import Test
import ADPCM

'''
Part 1: Read audio file into vector x.
'''


def test(src, dst, bits):
    try:
        source_read = wave.open(src, 'r')
        source_write = wave.open(dst, 'w')
    except FileNotFoundError:
        print('Failed to open files!')
        return False

    channel = source_read.getnchannels()
    width = source_read.getsampwidth()
    rate = source_read.getframerate()
    print("channels: " + str(channel))
    print("width:" + str(width))
    print("rate: " + str(rate))

    n_frames = source_read.getnframes()
    wave_data = source_read.readframes(n_frames)
    if not (bits == 8 or bits == 16):
        raise TypeError("Wrong bits type!")

    bits = int(bits / 8)

    # u-law compress
    u_law_data = audioop.lin2ulaw(wave_data, 1)
    compress_data = audioop.ulaw2lin(u_law_data, 1)
    adpcm = audioop.lin2adpcm(wave_data, 1, None)
    # print(adpcm)

    # source_write.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    source_write.setparams((channel, width, rate, 0, 'NONE', 'Test'))
    source_write.writeframes(adpcm[0])

    source_read.close()
    source_write.close()
    print("Data has already written into file!")
    adpcm[0] = adpcm[0].decoding('utf-8')
    return adpcm


def convert_to_8_bits(src, dst, bits):
    """

    :param src:
    :param bits:
    :return: u-law data
    """
    try:
        source_read = wave.open(src, 'r')
        source_write = wave.open(dst, 'w')
    except FileNotFoundError:
        print('Failed to open files!')
        return False

    channel = source_read.getnchannels()
    width = source_read.getsampwidth()
    rate = source_read.getframerate()
    print("channels: " + str(channel))
    print("width:" + str(width))
    print("rate: " + str(rate))

    n_frames = source_read.getnframes()
    wave_data = source_read.readframes(n_frames)
    if not (bits == 8 or bits == 16):
        raise TypeError("Wrong bits type!")

    bits = int(bits / 8)

    # u-law compress
    u_law_data = u_law_e(wave_data)
    # source_write.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    source_write.setparams((channel, width, rate, 0, 'NONE', 'Test'))
    source_write.writeframes(u_law_data)

    source_read.close()
    source_write.close()
    print("Data has already written into file!")
    # adpcm[0] = adpcm[0].decoding('utf-8')
    return u_law_data


def read_wav(path='8bits.wav'):
    """
    Plot given audio file
    :return: None
    """
    f = read(path)
    arr = np.array(f[1], dtype='int64')

    # plt.plot(arr)
    # plt.savefig('Wave.png')
    # plt.show()
    return arr


def plot_arr(arr):
    plt.plot(arr)
    plt.savefig('Wave.png')
    plt.show()


if __name__ == '__main__':
    # arr = read_wav('./Audio/LDC93S1.wav')
    audio = uLaw
    #
    # en = audio.u_law_encode(arr)
    # plot_arr(en)
    #
    # de = audio.u_law_decode(en)
    # plot_arr(de)

    adpcm = ADPCM
    en = read_wav('8bits.wav')

    # Apply ADPCM encoder to compressed data
    adpcm_en = adpcm.encoder(en)
    plot_arr(adpcm_en)

    # Apply ADPCM decoder to encode data
    adpcm_de = adpcm.decoder(adpcm_en)
    plot_arr(adpcm_de)

    # Apply u-Law expansion to the decoded data
    final_de = audio.u_law_decode(adpcm_de)
    plot_arr(final_de)
