#-*- coding: utf-8 -*-
"""
    Enable or disable devices from X using xinput
"""
import signal
import os

disabled_ids = []


def get_ids():
    return [id.replace('\n', '') for id in os.popen('xinput list --id-only').readlines()]


def get_device_from_id(id):
    return os.popen('xinput --list-props {0} | grep "Device Node"'.format(id)).read().split(':')[-1].strip().replace('"', '')


def get_devices_to_id_dict():
    return dict([(get_device_from_id(id), id) for id in get_ids()])


def get_id_from_device(device):
    device = os.path.realpath(device)
    device_to_id = get_devices_to_id_dict()
    return device_to_id.get(device, '')


def disable_id(id):
    os.popen('xinput disable {0}'.format(id))
    disabled_ids.append(id)


def enable_id(id):
    os.popen('xinput enable {0}'.format(id))


def disable_device(device):
    disable_id(get_id_from_device(device))


def enable_device(device):
    enable_id(get_id_from_device(device))


def __trap_handler(signum, frame):
    for id in disabled_ids:
        enable_id(id)

signal.signal(signal.SIGTERM, __trap_handler)
signal.signal(signal.SIGINT, __trap_handler)
