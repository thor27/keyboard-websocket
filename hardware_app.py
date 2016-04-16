#-*- coding: utf-8 -*-

import evdev
import xinput

from socketIO_client import SocketIO

def read_keyboard(device, ws):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)

            ws.emit('hardware_event', {
                'type': get_type(key_event),
                'data': key_event.keycode
            })
            print get_type(key_event), key_event.keycode

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

with SocketIO('localhost', 5000) as ws:
    device_filename = load_device_filename()
    device = evdev.InputDevice(device_filename)
    xinput.disable_device(device_filename)
    read_keyboard(device, ws)
