# -*- coding: utf-8 -*-
"""Scale keyboard USB device input.

Reads keyboard events from the GRAM scale USB keyboard device.
The script waits for the USB device to become available again, in case it has been disconnected.
Also, it grabs the device exclusively such that no keyboard presses get emitted to the Linux
console, causing failed login attempts.
Each read line gets emitted to STDOUT. Log information is written to STDERR.

The script is part of the "IoT Kaffeekanne" project, lecture 'Internet of Things' of the Reutlingen
University (HHZ), SoSe 2016.

"""

import sys
import logging
import evdev
import pyudev
import datetime
import time
import json

import ibmiotf.device

from threading import Thread
from Queue import Queue

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s [%(levelname)s] %(message)s')

# The GRAM scale USB keyboard adapter
DEFAULT_USB_VENDOR_ID = 'c216'
DEFAULT_USB_PRODUCT_ID = '0109'

# Worker thread settings
QUEUE_MEASUREMENTS_WORKER_INTERVAL = 1
QUEUE_PAYLOAD_WORKER_INTERVAL = 30

# Global queue variable
queue_measurements = Queue()
queue_payload = Queue()

# Define the IBM Watson IoT client
ibm_client = None

def validate_device(device, product_id=DEFAULT_USB_PRODUCT_ID, vendor_id=DEFAULT_USB_VENDOR_ID):
    """Validate if the given device is the scale.

    Args:
        device(pyudev.Device): The device object to validate.
        product_id(Optional[str]): The USB product id, defaults to the GRAM scale product id.
        vendor_id(Optional[str]): The USB vendor id, defaults to the GRAM scale vendor id.

    Returns:
        bool: True if the given device object is the scale, False otherwise.

    """
    parent = device.find_parent('usb', 'usb_device')
    if not parent:
        return False
    if (parent.attributes.get('idProduct') != product_id or
            parent.attributes.get('idVendor') != vendor_id):
        return False
    if not 'DEVNAME' in device:
        return False
    return True

def wait_for_scale(product_id=DEFAULT_USB_PRODUCT_ID, vendor_id=DEFAULT_USB_VENDOR_ID):
    """Wait for the scale to be plugged-in.

    Uses a Linux udev monitor to wait for the scale to be plugged-in. This is useful to exclusively
    fetch the input device afterwards, to avoid the scale keyboard device to spam the console with
    keyboard presses.

    Args:
        product_id(Optional[str]): The USB product id, defaults to the GRAM scale product id.
        vendor_id(Optional[str]): The USB vendor id, defaults to the GRAM scale vendor id.

    Returns:
        str: The device name of the scale, for example '/dev/input/event10'.

    """
    logging.info('Waiting for scale to be plugged-in')
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('input')
    for device in iter(monitor.poll, None):
        if device.action != 'add':
            continue
        if not validate_device(device, product_id, vendor_id):
            continue
        logging.info('Scale has been plugged-in! Device name: %s', device['DEVNAME'])
        return device['DEVNAME']

def get_scale_device(product_id=DEFAULT_USB_PRODUCT_ID, vendor_id=DEFAULT_USB_VENDOR_ID):
    """Get the scale device name from the list of plugged-in devices.

    Args:
        product_id(Optional[str]): The USB product id, defaults to the GRAM scale product id.
        vendor_id(Optional[str]): The USB vendor id, defaults to the GRAM scale vendor id.

    Returns:
        str: The device name of the scale, for example '/dev/input/event10'.
        ``None`` if the scale is not yet connected to the computer.

    """
    context = pyudev.Context()
    for device in context.list_devices(subsystem='input'):
        if not validate_device(device, product_id, vendor_id):
            continue
        logging.info('Scale is already plugged-in! Device name: %s', device['DEVNAME'])
        return device['DEVNAME']
    logging.info('Scale is not plugged-in!')
    return None

def read_from_device(devname, handler):
    """Read keyboard events from the device with the given name.

    Args:
        devname(str): The name of the device to read from, e.g. '/dev/input/event10'.
        handler(func): Handler function that will be called for each read key event.

    Raises:
        IOError: If no more events can be read, e.g. if the scale is unplugged.
    """
    device = evdev.InputDevice(devname)
    logging.info('Exclusively grabbing device %s', devname)
    device.grab()
    logging.info('Starting to read keyboard events from device %s', devname)
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            handler(evdev.KeyEvent(event))

class LineForwarder:
    """Handle key events and forward complete lines to STDOUT"""
    def __init__(self):
        self.line = ''
        self.char_map = {}
        self.mode = 'NORMAL'
        for i in range(0, 10):
            self.char_map['KEY_{}'.format(str(i))] = str(i)

    def forward(self):
        """Queue up current line"""
        queue_measurements.put(self.line)

    def handle_event(self, event):
        """Handle the given keyboard event."""
        if not event.keystate == evdev.KeyEvent.key_up:
            return
        if event.keycode == 'KEY_ENTER':
            self.forward()
            self.line = ''
            self.mode = 'NORMAL'
            return
        if event.keycode == 'KEY_RIGHTSHIFT':
            self.mode = 'RIGHTSHIFT'
            return
        if self.mode == 'RIGHTSHIFT':
            # Ignore keys after KEY_RIGHTSHIFT has been pressed ... until
            # KEY_ENTER be pressed
            return
        if event.keycode in self.char_map and self.mode == 'NORMAL':
            self.line += self.char_map[event.keycode]

def queue_measurements_worker(q):
    """Worker thread to handle queued measurements."""
    while True:
        qsize = q.qsize()
        if qsize > 0:
            measurements = []
            while not q.empty():
                measurement = q.get()
                q.task_done()
                if measurement == '':
                    continue
                measurements.append(int(measurement))
            logging.info('Handling [%s] measurements: %s' % (qsize, json.dumps(measurements)))
            payload = {
                'timestamp': int(time.time()),
                'measurements': measurements
            }
            queue_payload.put(payload)
            time.sleep(QUEUE_MEASUREMENTS_WORKER_INTERVAL)

def queue_payload_worker(q):
    """Worker thread to handle queued payloads."""
    while True:
        if q.qsize() > 0:
            payloads = []
            while not q.empty():
                payloads.append(q.get())
                q.task_done()
            logging.info('Sending payload containing [%s] measurements' % q.qsize())
            logging.debug(json.dumps(payloads))
            ibm_client.connect()
            ibm_client.publishEvent('measurements', 'json', payloads, 2)
            time.sleep(QUEUE_PAYLOAD_WORKER_INTERVAL)

def main():
    """Get the scale keyboard device and read key events."""
    worker = Thread(target=queue_measurements_worker, args=(queue_measurements,))
    worker.setDaemon(True)
    worker.start()
    worker = Thread(target=queue_payload_worker, args=(queue_payload,))
    worker.setDaemon(True)
    worker.start()
    while True:
        devname = get_scale_device()
        if not devname:
            devname = wait_for_scale()
        try:
            forwarder = LineForwarder()
            read_from_device(devname, forwarder.handle_event)
        except IOError:
            logging.info('Scale has been disconnected!')

if __name__ == '__main__':
    try:
        options = {
            'org': 'xasyuj',
            'type': 'gram-rz-30k',
            'id': '2',
            'auth-method': 'token',
            'auth-token': 'JJ31YWRi@EksUeoKQ+'
        }
        ibm_client = ibmiotf.device.Client(options)
        main()
    except ibmiotf.ConnectionException as e:
        logging.info('Error connecting to IBM Watson IoT Platform: %s' % e.value)
    except KeyboardInterrupt:
        logging.info('Script interrupted, program will exit')
        sys.exit()
