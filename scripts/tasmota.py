#!/usr/bin/env python

import logging
from json import loads
from time import sleep
from threading import Thread
from requests import get
from requests.exceptions import ConnectionError
from artemisremotecontrol.config import Config
from artemisremotecontrol import getleds, setleds

try:
    config_name = __name__.split('.')[1]
except IndexError:
    getleds()
    print('I created a leds.json in scripts/. Check this file and edit config.json to your needs.')
    print('Run run.py after config.')
    exit()

    # Code, I'm not sure to use
    # Would need to cd out of scripts/
    # And not sure if it is easier to config that way instead of writing directly in the file
    config_name = __file__.split('\\')[-1].split('.')[0]
    logging.debug(config_name)
    config = Config()
    config.load(config_name)
    done = False
    while not done:
        url = input('Enter the URL to your tasmota-device, with credentials, like: http://192.168.4.123/cm?cmnd=Power&user=admin&password=pw')
        key = input('Enter the key of the value, like POWER in {\'POWER\': \'ON\':\n')
        value = input('Enter the value, like ON in {\'POWER\': \'ON\':\n')
        done_devices = False
        device_index = 1
        devices = list()
        print('Look in scripts/leds.json for the LEDs and devices.')
        while not done_devices:
            user_input = input(f'Type the device id of the {device_index}. led. Leave empty after you are done:\n')
            device_index += 1
            if user_input:
                devices.append(user_input)
            else:
                done_devices = True
        done_leds = False
        led_index = 1
        leds = list()
        print('Look in scripts/leds.json for the LEDs and devices.')
        while not done_leds:
            user_input = input(f'Type the led id of the {led_index}. led. Leave empty after you are done:\n')
            led_index += 1
            if user_input:
                leds.append(user_input)
            else:
                done_leds = True
        color1 = input('Enter the color for the state/value you choose earlier in format #ffffff:\n')
        color2 = input('Enter the color for the other state in format #ffffff:')
        color3 = input('Enter the color for the disconnected state in format #ffffff:\n')
        config.add(config_name, [url, key, value, devices, leds, color1, color2, color3])
        more = input('Saved. If you want to add another device, type \'y\', otherwise leave empty and press enter.\n')
        if not more:
            done = True
    print('Run run.py now.')
    exit()


def loop():
    while True:
        for device in config.config[config_name]:
            url, keyword, string, devices, leds, color_on, color_off, color_dc = device

            try:
                response = get(url, timeout=1)
                status = response.status_code
            except ConnectionError:
                status = False
            if status != 200:
                # send "Disconnected" state
                logging.debug('Can\'t connect to device')
                setleds(devices, leds, color_dc)
                continue

            text = loads(response.content.decode('utf-8'))
            logging.debug(text)
            if text[keyword] == string:
                # Send "true" state
                logging.debug('Found searching string')
                setleds(devices, leds, color_on)
            else:
                # Send "false" state
                logging.debug('Not found searching string')
                setleds(devices, leds, color_off)
            sleep(1)
        sleep(5)


logging.basicConfig(level=logging.WARNING)
config = Config()
config.load(config_name)
tloop = Thread(target=loop)
tloop.start()
