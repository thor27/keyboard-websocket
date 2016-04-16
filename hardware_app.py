#-*- coding: utf-8 -*-

import evdev
import xinput
import argparse
import sys
import os
from socketIO_client import SocketIO


def read_keyboard(device, ws, silent=False):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)

            ws.emit('hardware_event', {
                'type': get_type(key_event),
                'data': key_event.keycode
            })
            if not silent:
                print(get_type(key_event), key_event.keycode)


def load_device_filename(keyboard_config_file):
    with open(keyboard_config_file) as config:
        filename = config.read().replace('\n', '')
    return filename


def get_type(key_event):
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
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', help='Don\'t print to stdout')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    if args.device_filename:
        device_filename = args.device_filename
    else:
        device_filename = load_device_filename(args.keyboard_config_file)

    device = evdev.InputDevice(device_filename)
    xinput.disable_device(device_filename)
    with SocketIO(args.hostname, args.port) as ws:
        read_keyboard(device, ws, args.silent)


if __name__ == '__main__':
    main()
