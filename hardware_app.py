

import evdev

device = evdev.InputDevice('/dev/input/by-id/usb-USB_USB_Keykoard-event-kbd')

from socketIO_client import SocketIO

def read_keyboard(ws):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)

            ws.emit('hardware_event', {
                'type': get_type(key_event),
                'data': key_event.keycode
            })
            print get_type(key_event), key_event.keycode

def get_type(key_event):
    if key_event.key_down:
        return 'KEY_DOWN'
    if key_event.key_up:
        return 'KEY_UP'
    if key_event.key_hold:
        return 'KEY_HOLD'

with SocketIO('localhost', 5000) as ws:
    read_keyboard(ws)
