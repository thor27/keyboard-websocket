 #-*- coding: utf-8 -*-

import evdev
from time import sleep
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
open_devices = [evdev.InputDevice(device.fn) for device in devices]

print 'Please wait... Do NOT press any key right now, cleaning up inputs...'
sleep(1)
for num,device in enumerate(open_devices):
    max_count = 5
    while device.read_one():
        max_count -= 1
        if not max_count:
            print 'Device', open_devices[num], 'seems to busy, removing!'
            del open_devices[num]
            break

print 'Thanks.'
print 'Now, press any key on the correct keyboard'

correct_device = None
while True:
    for num,device in enumerate(open_devices):
        if device.read_one():
            correct_device = device
            break
    if correct_device:
        break

with open('keyboard.cfg', 'w') as config:
    config.write(device.fn + '\n')

print 'Done, correct device is:', device
