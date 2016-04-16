 #-*- coding: utf-8 -*-

import evdev
import sys
import argparse
from time import sleep

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
open_devices = [evdev.InputDevice(device.fn) for device in devices]


def clean_up():
    print 'Please wait... Do NOT press any key right now, cleaning up inputs...'
    sleep(1)
    for num, device in enumerate(open_devices):
        max_count = 5
        while device.read_one():
            max_count -= 1
            if not max_count:
                print 'Device', open_devices[num], 'seems too busy, removing!'
                del open_devices[num]
                break
    print 'Thanks.'


def detect_key():
    print 'Now, press any key on the correct keyboard'
    while True:
        for num, device in enumerate(open_devices):
            if device.read_one():
                return device


def parse_args(args):
    parser = argparse.ArgumentParser(description='Detect keyboard device.')
    parser.add_argument('-o', '--file-output', dest='outfile', type=str, default='keyboard.cfg', help='Output file (Default: keyboard.cfg)')
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    clean_up()
    device = detect_key()

    with open(args.outfile, 'w') as outfile:
        outfile.write(device.fn + '\n')

    print 'Done, correct device is:', device


if __name__ == '__main__':
    main()
