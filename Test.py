__author__ = 'BorisMirage'
# --- coding:utf-8 ---

'''
Create by BorisMirage
File Name: Test
Create Time: 11/20/18 18:06
'''
from scipy.io.wavfile import read
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import os
import audioop
import wave
import math


class AudioCoding(object):
    # def __init__(self, path='./Audio/LDC93S1.wav'):
    #     """
    #     Pass audio file path to class.
    #     :param path: file path
    #     """
    #     self.path = path

    @staticmethod
    def plot_file(path='./Audio/LDC93S1.wav'):
        """
        Plot given audio file
        :return: None
        """
        f = read(path)
        arr = np.array(f[1], dtype=float)
        plt.plot(arr)
        plt.savefig('Wave.png')
        plt.show()

    @staticmethod
    def u_law_compressor(path='./Audio/LDC93S1.wav', quantization_steps=256, bit_format="16bit_pcm"):
        """
        Implement u-law compression.

        :param path: file name
        :param quantization_steps: steps for quantization
        :param bit_format: bit number
        :return: quantized signal and signal's sampling rate
        """
        sampling_rate, signal = wavfile.read(path)

        # discard R channel to convert to mono if necessary
        if len(signal.shape) > 1:
            signal = signal[:, 0].astype(float)

        # normalize to -1 ~ 1
        if bit_format == "16bit_pcm":
            max = 1 << 15
        elif bit_format == "32bit_pcm":
            max = 1 << 31
        elif bit_format == "8bit_pcm":
            max = 1 << 7
        else:
            raise TypeError("Wrong bit format!")

        # signal_1 = np.array(signal / max, dtype=float)
        print(max)
        signal_1 = signal / max
        print(signal_1)

        # mu-law companding transformation
        mu = quantization_steps - 1
        signal_1 = np.sign(signal_1) * np.log(1 + mu * np.absolute(signal_1)) / np.log(1 + mu)

        # quantize
        quantized_signal = (np.clip(signal_1 * 0.5 + 0.5, 0, 1) * mu).astype(np.float)

        # remove silence signals
        # silence_threshold = 1
        # for start in range(0, quantized_signal.size):
        #     if abs(quantized_signal[start] - 127) > silence_threshold:
        #         break
        # for end in range(1, quantized_signal.size):
        #     if abs(quantized_signal[-end] - 127) > silence_threshold:
        #         break
        # quantized_signal = quantized_signal[start:-end]

        return quantized_signal, sampling_rate

    @staticmethod
    def u_law_decompressor(quantized_signal, save_name='Test.wav', quantization_steps=256, bit_format="16bit_pcm",
                           sampling_rate=16000):
        """
        Decompress audio file and save audio to audio file.
        :param quantized_signal: u-law transferred signal
        :param save_name: save file name
        :param quantization_steps: steps for quantization
        :param bit_format: bit number
        :param sampling_rate: signal sampling rate
        :return: None
        """
        quantized_signal = quantized_signal.astype(float)
        normalized_signal = (quantized_signal / quantization_steps - 0.5) * 2.0

        # inv mu-law
        mu = quantization_steps - 1
        signals_1d = np.sign(normalized_signal) * ((1 + mu) ** np.absolute(normalized_signal)) / mu

        if bit_format == "16bit_pcm":
            max = 1 << 15
            type = np.int16
        elif bit_format == "32bit_pcm":
            max = 1 << 31
            type = np.int32
        elif bit_format == "8bit_pcm":
            max = 1 << 7
            type = np.uint8
        else:
            raise TypeError("Wrong bit format!")

        signals_1d *= max

        audio = signals_1d.reshape((-1, 1)).astype(type)
        audio = np.repeat(audio, 2, axis=1)
        wavfile.write(save_name, sampling_rate, audio)
        return signals_1d


def downsampleWav(src, dst, inrate=44100, outrate=16000, inchannels=2, outchannels=1):
    if not os.path.exists(src):
        print('Source not found!')
        return False

    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
    except FileNotFoundError:
        print('Failed to open files!')
        return False

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)

    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1:
            converted = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print('Failed to down sample wav!')
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted)
    except:
        print('Failed to write wav!')
        return False

    try:
        s_read.close()
        s_write.close()
    except IOError:
        print('Failed to close wav files!')
        return False

    return True


def test_u_law(vector, max):
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

        up = math.log(1 + u * abs(vector[i] / max))

        out[i] = sign * (math.log(1 + u * abs(vector[i] / max)) / de)

        # print(abs(vector[i] / max))
    print(out)
    return out
