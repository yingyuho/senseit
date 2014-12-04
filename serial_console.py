#! /usr/bin/env python
import serial

def init(env, port):
    env['ser'] = serial.Serial(port, baudrate=38400, timeout=0.1)

def done(env):
    env['ser'].close()

def main():
    env = {}
    init(env, '/dev/tty.usbmodem1421')

    data = None

    while True:
        data = raw_input('> ')
        if data != 'exit':
            env['ser'].write(data + '\n')
            print(env['ser'].read(10))
        else:
            break

    done(env)

if __name__ == '__main__':
    main()