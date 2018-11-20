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


def read_file():
    """
    Read file
    :return: read vector x
    """
    f = read("./Audio/LDC93S1.wav")
    arr = np.array(f[1], dtype=float)
    return arr


def plot(arr):
    """
    Plot array based on given file.
    :param arr: array to plot
    :return: None
    """
    plt.plot(arr)
    plt.savefig('Wave.png')
    plt.show()
    return



if __name__ == '__main__':
    plot(read_file())