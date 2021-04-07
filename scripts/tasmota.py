#!/usr/bin/env python

import logging
from json import loads
from time import sleep
from threading import Thread
from requests import get
from requests.exceptions import ConnectionError, ChunkedEncodingError
from artemisremotecontrol.config import Config
from artemisremotecontrol import getleds, setleds

try:
    config_name = __name__.split('.')[1]
except IndexError:
    getleds()
    print('I created a leds.json. Check this file and edit config.json to your needs.')
    print('Run run.py after config.')
    exit()


def loop():
    while True:
        for device in config.config[config_name]:
            for uri in device['data']:
                url = device['base_url'] + uri['uri']
                try:
                    response = get(url, timeout=1)
                    status = response.status_code
                except (ConnectionError, ChunkedEncodingError):
                    status = False
                if status != 200:
                    # send "Disconnected" state
                    logging.debug('Can\'t connect to device')
                    setleds(uri['devices'], uri['leds'], uri['colors'][2])
                    continue

                text = loads(response.content.decode('utf-8'))
                logging.debug(text)
                if isinstance(uri['value'], list):
                    percent = (int(text[uri['key']]) - uri['value'][0])/((uri['value'][1] - uri['value'][0])/100)
                    logging.debug(f'Percent: {percent}')
                    if len(uri['leds']) == 1:
                        decimal = 255 / 100 * percent  # 255 is FF in hex
                        alpha = f'#{hex(decimal)}'
                        ocolor = uri['colors'][0].replace('#', '')
                        color = f'{alpha}{ocolor}'
                        setleds(uri['devices'], uri['leds'], color)
                    else:
                        setleds(uri['devices'], uri['leds'], uri['colors'][1])
                        led_count = len(uri['leds'])
                        led_light = (led_count / 100) * percent
                        devices = list()
                        leds = list()
                        logging.debug(led_count)
                        logging.debug(led_light)
                        for led in range(int(led_light)):
                            devices.append(uri['devices'][led])
                            leds.append(uri['leds'][led])
                        setleds(devices, leds, uri['colors'][0])
                else:
                    if text[uri['key']] == uri['value']:
                        # Send "true" state
                        logging.debug('Found searching string')
                        setleds(uri['devices'], uri['leds'], uri['colors'][0])
                    else:
                        # Send "false" state
                        logging.debug('Not found searching string')
                        setleds(uri['devices'], uri['leds'], uri['colors'][1])
            sleep(1)
        sleep(5)


def save():
    device = dict()
    device['base_url'] = 'http://192.168.1.12/cm?user=admin&password=pw&cmnd='
    device['data'] = list()
    # Range based values
    device['data'].append(dict())
    device['data'][-1]['uri'] = 'Dimmer'
    device['data'][-1]['key'] = 'Dimmer'
    device['data'][-1]['value'] = [15, 60]  # make sure, that these are integers
    device['data'][-1]['devices'] = [  # if you use only one led here, the opacity will be the range indicator
        'Logitech G910v2-Logitech-G910v2-Keyboard',
        'Logitech G910v2-Logitech-G910v2-Keyboard',
        'Logitech G910v2-Logitech-G910v2-Keyboard',
        'Logitech G910v2-Logitech-G910v2-Keyboard'
    ]
    device['data'][-1]['leds'] = [
        'Keyboard_Programmable6',
        'Keyboard_Programmable7',
        'Keyboard_Programmable8',
        'Keyboard_Programmable9'
    ]
    device['data'][-1]['colors'] = [
        '#0000FF',  # active color, omit alpha value if you use only one key
        '#821700',  # the "background"
        '#000000'
    ]
    # bool values
    device['data'].append(dict())
    device['data'][-1]['uri'] = 'Power'
    device['data'][-1]['key'] = 'POWER'
    device['data'][-1]['value'] = 'ON'
    device['data'][-1]['devices'] = [
        'Logitech G910v2-Logitech-G910v2-Keyboard'
    ]
    device['data'][-1]['leds'] = [
        'Keyboard_Programmable4'
        ]
    device['data'][-1]['colors'] = [
        '#0000FF',
        '#821700',
        '#000000'
    ]

    config.add(config_name, device)
    logging.warning('Saved.')


config = Config()
config.load(config_name)
# Change the values in save() and uncomment these two lines, run run.py *once* and comment them again
#save()
#exit()
tloop = Thread(target=loop)
tloop.start()
