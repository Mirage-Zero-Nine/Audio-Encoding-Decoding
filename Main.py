__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: Main.py
Create Time: 11/20/18 11:34
'''

from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Own lib
import uLaw
import ADPCM
import Quantization
import time


def date_string():
    """
    Generate current date and time as file name.
    :return: current date time in string format
    """
    # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    now = time.time() * 1000.0
    return str(now)


def read_wav(path='8bits.wav'):
    """
    Read wav file into a numpy array.
    :return: numpy array
    """
    f = read(path)
    arr = np.array(f[1], dtype='int64')

    return arr


def plot_arr(arr, title):
    """
    Plot given numpy array
    :param arr: numpy array
    :param title: plot title
    :return: None
    """
    # plt.plot(arr, 'c')
    # plt.title(title)
    # plt.savefig(date_string() + '.png')
    # plt.show()
    bg_color = 'black'
    fg_color = 'white'

    fig = plt.figure(facecolor=bg_color, edgecolor=fg_color)
    axes = fig.add_subplot(111)
    axes.patch.set_facecolor(bg_color)
    axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
    axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
    for spine in axes.spines.values():
        spine.set_color(fg_color)

    plt.title(title, color=fg_color)
    plt.plot(arr, 'g', axes=axes)
    # plt.xlabel('$$', color=fg_color)
    # plt.ylabel('', color=fg_color)
    plt.savefig(date_string() + '.png')

    plt.show()
    plt.close()


def main_fun():
    wav_rate, wav_arr = read('LDC93S1.wav')
    # print(wav_rate)
    # print(wav_arr)
    plot_arr(wav_arr, 'Original Wave Signal in 16 bit')

    # Quantization 16 bits
    q = Quantization.quantization(wav_arr, 32768, 'float')
    # plot_arr(q, 'Quantized 16 bit')

    de_q = Quantization.inverse_quantization(q, 128, 'int')
    plot_arr(de_q, '8 bits')

    ulaw_compressed = uLaw.u_law_compress(q)
    plot_arr(ulaw_compressed, 'Apply u-Law compression to 16 bits data')

    ulaw_compressed_quantized = Quantization.quantization(ulaw_compressed, np.amax(ulaw_compressed))
    plot_arr(ulaw_compressed_quantized, 'u-law compressed data quantization')

    # ulaw_decompressed = uLaw.u_law_expend(ulaw_compressed_quantized, np.amax(q))
    # plot_arr(ulaw_decompressed, 'u-law expansion')

    convert_to_8_bit = Quantization.inverse_quantization(ulaw_compressed_quantized, 128, 'int')
    plot_arr(convert_to_8_bit, 'Inverse quantize u-law compressed data to 8 bits')

    # write('8-bit.wav', wav_rate, bit_8)

    adpcm_encoding = ADPCM.encoder(convert_to_8_bit)
    plot_arr(adpcm_encoding, 'ADPCM encoding')

    adpcm_decoding = ADPCM.decoder(adpcm_encoding)
    plot_arr(adpcm_decoding, 'ADPCM decoding')

    adpcm_decoding_quantized = Quantization.quantization(adpcm_decoding, 128, 'float')

    ulaw_decompressed_adpcm = uLaw.u_law_expend(adpcm_decoding)
    plot_arr(ulaw_decompressed_adpcm, 'u-law expansion ADPCM decoding')

    write('Reconstructed.wav', wav_rate, ulaw_decompressed_adpcm)


if __name__ == '__main__':
    main_fun()
