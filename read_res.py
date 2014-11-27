#! /usr/bin/env python
from __future__ import print_function
from sys import stdout
import serial

def align(f):
    count = 0
    while True:
        if f.read() == '\xff':
            count += 1
        else:
            count = 0
        if count >= 4:
            break

def encode_int(s):
    ret = 0
    shift = 0
    for c in s:
        ret += ord(c) << shift
        shift += 8
    return ret

def res8(f):
    res = []
    for i in range(8):
        res.append(encode_int(f.read(2)))
    for r in res:
        print('{:04d}'.format(r), end=' ')
    print()
    stdout.flush()

def time(f):
    t = encode_int(f.read(4))
    print('time = {}'.format(t))

def main():

    data = None

    port = '/dev/tty.usbmodem1411'

    with serial.Serial(port, baudrate=115200, timeout=1) as ser:
        while True:
            align(ser)
            pkt_id = ser.read(4)
            if pkt_id == 'res8':
                res8(ser)
            elif pkt_id == 'time':
                time(ser)

if __name__ == '__main__':
    main()