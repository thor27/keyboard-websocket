#-*- coding: utf-8 -*-

import evdev
import xinput
import json
import sys
from time import sleep
from websocket import create_connection, socket


def read_keyboard(device, ws):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            event_data = {
                'type': get_type(key_event),
                'keycode': key_event.keycode
            }
            ws.send(json.dumps(event_data))
            print(event_data)


def load_device_filename():
    with open('keyboard.cfg') as config:
        filename = config.read().replace('\n','')
    return filename


def get_type(key_event):
    if key_event.keystate == key_event.key_down:
        return 'DOWN'
    if key_event.keystate == key_event.key_up:
        return 'UP'
    if key_event.keystate == key_event.key_hold:
        return 'HOLD'


def main(port):
    url = "ws://localhost:{0}/broadcast/websocket".format(port)
    ws = None
    try:
        ws = create_connection(url)
        device_filename = load_device_filename()
        device = evdev.InputDevice(device_filename)
        xinput.disable_device(device_filename)
        read_keyboard(device, ws)
    finally:
        if ws:
            ws.close()


if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else '8000'
    main(port)
