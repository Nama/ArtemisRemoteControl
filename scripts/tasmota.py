#!/usr/bin/env python

import logging
from json import loads
from asyncio import run, sleep
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


async def loop():
    while True:
        data = {}
        for device in config.config[config_name]:
            for uri in device['data']:
                url = device['base_url'] + uri['uri']
                if not uri['uri'] in data:
                    data[uri['uri']] = {}
                try:
                    response = get(url, timeout=0.3)
                    status = response.status_code
                except (ConnectionError, ChunkedEncodingError, ReadTimeout):
                    status = False
                if status != 200:
                    # send "Disconnected" state
                    logging.debug('Can\'t connect to device')
                    data[uri['uri']][device['name']] = 'down'
                    continue

                response_content = loads(response.content.decode('utf-8'))
                logging.debug(response_content)
                value = response_content[uri['key']]
                logging.debug(f'Value: {value}')
                data[uri['uri']][device['name']] = value
            await sleep(0.1)
        await setleds(config_name, data)
        await sleep(5)


def save():
    device = dict()
    device['name'] = 'Dimmer'
    device['base_url'] = 'http://192.168.1.13/cm?user=admin&password=pw&cmnd='
    device['data'] = list()
    # change values if needed, only for adding to the config.json
    device['data'].append(dict())
    device['data'][-1]['uri'] = 'Power'
    device['data'][-1]['key'] = 'POWER'

    config.add(config_name, device)
    logging.info('Saved.')


config = Config()
config.load(config_name)
# Change the values in save() and uncomment these two lines, run run.py *once* and comment them again
#save()
#exit()
tloop = Thread(target=lambda: run(loop()))
tloop.start()
