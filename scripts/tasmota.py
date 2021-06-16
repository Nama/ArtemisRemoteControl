#!/usr/bin/env python

import logging
from json import loads
from time import sleep
from threading import Thread
from requests import get
from requests.exceptions import ConnectionError, ChunkedEncodingError, ReadTimeout
from artemisremotecontrol.config import Config
from artemisremotecontrol import setleds

try:
    config_name = __name__.split('.')[1]
except IndexError:
    print('Run run.py after config.')
    exit()


def loop():
    while True:
        for device in config.config[config_name]:
            for uri in device['data']:
                url = device['base_url'] + uri['uri']
                try:
                    response = get(url, timeout=0.3)
                    status = response.status_code
                except (ConnectionError, ChunkedEncodingError, ReadTimeout):
                    status = False
                if status != 200:
                    # send "Disconnected" state
                    logging.debug('Can\'t connect to device')
                    setleds(f'{device["name"]}{uri["uri"]}', 'down')
                    continue

                text = loads(response.content.decode('utf-8'))
                logging.debug(text)
                value = text[uri['key']]
                logging.debug(f'Value: {value}')
                setleds(f'{device["name"]}{uri["uri"]}', value)
            sleep(0.1)
        sleep(5)


def save():
    device = dict()
    device['name'] = 'Dimmer'
    device['base_url'] = 'http://192.168.1.13/cm?user=admin&password=pw&cmnd='
    device['data'] = list()
    # Range based values, comment if not needed
    device['data'].append(dict())
    device['data'][-1]['uri'] = 'Dimmer'
    device['data'][-1]['key'] = 'Dimmer'
    device['data'][-1]['value'] = None
    # bool values
    device['data'].append(dict())
    device['data'][-1]['uri'] = 'Power'
    device['data'][-1]['key'] = 'POWER'
    device['data'][-1]['value'] = 'ON'

    config.add(config_name, device)
    logging.info('Saved.')


config = Config()
config.load(config_name)
# Change the values in save() and uncomment these two lines, run run.py *once* and comment them again
#save()
#exit()
tloop = Thread(target=loop)
tloop.start()
