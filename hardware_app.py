#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    Read device from evdev and send key events to websocket.
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
import xinput
import argparse
import sys
import os
import signal
import time
from socketIO_client import SocketIO


class KeyboardReader(object):
    def __init__(self, args):
        self.args = args
        if args.device_filename:
            self.device_filename = args.device_filename
        else:
            self.device_filename = self.load_device_filename()

        self.device = None
        self.ws = None

        signal.signal(signal.SIGTERM, self.__stop_app)
        signal.signal(signal.SIGINT, self.__stop_app)

        self.ws = SocketIO(args.hostname, args.port)
        if args.all_devices:
            self.read_all_keyboards()
        else:
            self.read_keyboard()

    def connect_keyboard(self):
        while True:
            try:
                if not self.args.silent:
                    print('Openning device {}...'.format(self.device_filename))
                self.device = evdev.InputDevice(self.device_filename)
                break
            except OSError:
                if not self.args.silent:
                    print('Can\'t open device. Waiting...')
                time.sleep(1)
        xinput.disable_device(self.device_filename)

        if not self.args.silent:
            print('Success!'.format(self.device_filename))


    def __stop_app(self, signum, frame):
        print('Trap called, exiting...')
        if self.device:
            self.device.close()

        if self.ws:
            self.ws._close()

        xinput.trap_handler(signum, frame)

        sys.exit(0)

    def get_all_devices(self):
        keyboards = os.popen('readlink -f /dev/input/by-path/*kbd').read().split('\n')
        devices = [evdev.InputDevice(fn) for fn in keyboards if fn]
        open_devices = []
        for device in devices:
            try:
                open_device = evdev.InputDevice(device.fn)
            except OSError:
                pass
            open_devices.append(open_device)
        return open_devices


    def send_ws_keyboard_list(self, open_devices):
        keyboard_package = [
            {
                'file':  keyboard.fn,
                'name': keyboard.name
            }
            for keyboard in open_devices
        ]

        if not self.args.silent:
            print(keyboard_package)

        self.ws.emit('devices_list', {
            'devices': keyboard_package
        })

    def read_all_keyboards(self):
        open_devices = self.get_all_devices()
        last_time = 0
        while True:
            if time.time() > last_time + 5:
                open_devices = self.get_all_devices()
                self.send_ws_keyboard_list(open_devices)
                last_time = time.time()

            for num, device in enumerate(open_devices):
                try:
                    event = device.read_one()
                except IOError:
                    open_devices = self.get_all_devices()
                    break
                if event:
                    self.process_event(event, device)

    def read_keyboard(self):
        while True:
            self.connect_keyboard()
            try:
                for event in self.device.read_loop():
                    self.process_event(event)
            except IOError:
                if not self.args.silent:
                    print('Device disconected!')

    def process_event(self, event, device=None):
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            package = {
                'type': self.get_type(key_event),
                'data': key_event.keycode
            }
            if device:
                package['device'] = {
                    'file': device.fn,
                    'name': device.name
                }

            self.ws.emit('hardware_event', package)

            if not self.args.silent:
                print(self.get_type(key_event), key_event.keycode)
                if device:
                    print(device.fn, device.name)

    def load_device_filename(self):
        with open(self.args.keyboard_config_file) as config:
            filename = config.read().replace('\n', '')
        return filename

    def get_type(self, key_event):
        if key_event.keystate == key_event.key_down:
            return 'DOWN'
        if key_event.keystate == key_event.key_up:
            return 'UP'
        if key_event.keystate == key_event.key_hold:
            return 'HOLD'


def parse_args(args):
    keyboardcfg = os.path.join(os.path.dirname(__file__), 'keyboard.cfg')
    parser = argparse.ArgumentParser(description='Send keyboard input to SocketIO')
    parser.add_argument('-f', '--config-file', dest='keyboard_config_file', type=str, default=keyboardcfg,
                        help='Keyboard Config File (Default: keyboard.cfg)')
    parser.add_argument('-d', '--device', dest='device_filename', type=str, default='',
                        help='Specify device to read. (Default: Read from Keyboard Config File)')
    parser.add_argument('-H', '--hostname', dest='hostname', type=str, default='localhost',
                        help='Specify socketIO hostname to connect. (Default: localhost)')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5000,
                        help='Specify socketIO port to connect. (Default: 5000)')
    parser.add_argument('-k', '--keep-keyboard-enabled', dest='disable_device', action='store_false',
                        help='Keep keyboard running without disabling on X11')
    parser.add_argument('-a', '--all-devices', dest='all_devices', action='store_true', help='Detect all devices keypresses and send device name to ws')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true',
                        help='Don\'t print to stdout')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    KeyboardReader(args)


if __name__ == '__main__':
    main()
