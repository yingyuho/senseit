#! /usr/bin/env python
from __future__ import print_function, division
from sys import stdin
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt

INTV = 2
PPS = 100
BIN_SIZE = 6

CHANNELS = (2, 3, 4)

def data_stream(f, channels, bin_size=1):
    getter = itemgetter(*channels)
    while True:
        buf = [None] * bin_size
        for i in range(bin_size):
            line = f.readline()
            # while True:
            nums = map(int, getter(line.split()))
            #     if all(x > 0 for x in nums):
            #         break
            buf[i] = nums
        ret = np.average(buf, axis=0)
        yield ret

def main():

    plt.ion()
    
    plt.figure()

    num_channels = len(CHANNELS)
    num_points = PPS * INTV + 1

    t = BIN_SIZE * np.linspace(-INTV, 0.0, num_points)
    data = np.zeros((num_channels, 2 * num_points - 1))
    cursor = 0

    lines = []

    for i in range(num_channels):
        plt.subplot(num_channels, 1, i + 1)
        line, = plt.plot(t, data[i][cursor : (cursor + num_points)])
        plt.ylim([0, 1023])
        lines.append(line)
        if i < num_channels - 1:
            line.axes.get_xaxis().set_visible(False)

    plt.draw()
    plt.show()

    for d in data_stream(stdin, CHANNELS, BIN_SIZE):
        print(d)
        # continue
        if cursor == num_points:
            data[:, : (num_points - 1)] = data[:, num_points :]
            cursor = 0
        data[:, (cursor + num_points - 1)] = d
        for i in range(num_channels):
            lines[i].set_ydata(
                data[i][cursor : (cursor + num_points)])
        plt.draw()
        cursor += 1

if __name__ == '__main__':
    main()