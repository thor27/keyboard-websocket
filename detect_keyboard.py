#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    Detect which keyboard to use, and saves in keyboard.cfg
    Copyright (C) 2016 Thomaz de Oliveira dos Reis <thor27@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function
import evdev
import sys
import argparse
import os
from time import sleep

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
open_devices = [evdev.InputDevice(device.fn) for device in devices]


def clean_up():
    print('Please wait... Do NOT press any key right now, cleaning up inputs...')
    sleep(1)
    for num, device in enumerate(open_devices):
        max_count = 5
        while device.read_one():
            max_count -= 1
            if not max_count:
                print('Device', open_devices[num], 'seems too busy, removing!')
                del open_devices[num]
                break
    print('Thanks.')


def detect_key():
    print('Now, press any key on the correct keyboard')
    while True:
        for num, device in enumerate(open_devices):
            if device.read_one():
                return device


def parse_args(args):
    keyboardcfg = os.path.join(os.path.dirname(__file__), 'keyboard.cfg')
    parser = argparse.ArgumentParser(description='Detect keyboard device.')
    parser.add_argument('-o', '--file-output', dest='keyboard_config_file', type=str, default=keyboardcfg,
                        help='Keyboard Config File (Default: keyboard.cfg)')
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    clean_up()
    device = detect_key()

    with open(args.keyboard_config_file, 'w') as outfile:
        outfile.write(device.fn + '\n')

    print('Done, correct device is:', device)


if __name__ == '__main__':
    main()
