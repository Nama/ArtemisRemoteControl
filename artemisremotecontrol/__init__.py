from requests import get, post
from requests.exceptions import ConnectionError, ChunkedEncodingError, ReadTimeout
import logging
from os import environ
from json import loads, dumps

logging.basicConfig(filename='error.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)


def _getapiurl(ep):
    txt_path = environ['ProgramData'] + '/Artemis/webserver.txt'
    url_endpoints = open(txt_path, 'r').readline() + 'plugins/endpoints'

    try:
        response = get(url_endpoints)
    except (ConnectionError, ChunkedEncodingError, ReadTimeout):
        logging.error('Can\'t connect to Artemis')
        return None
    if response.status_code != 200:
        return None
    endpoints = loads(response.content)
    url = ''
    for endpoint in endpoints:
        if endpoint['Name'] == ep:
            url = endpoint['Url']
            break
    if url:
        return url
    else:
        logging.error('Couldn\'t get endpoint URL')
        return None


def getleds():
    url = _getapiurl('GetLeds')
    if not url:
        return
    response = post(url)
    leds = loads(response.content)
    with open('leds.json', 'w') as leds_file:
        leds_file.writelines(dumps(leds, indent=4))


def setleds(deviceids: list, ledids: list, color: str):
    url = _getapiurl('SetLeds')
    if not url:
        return
    data = list()
    for i, led in enumerate(ledids):
        data.append({'DeviceId': deviceids[i], 'LedId': led, 'Color': color})
    logging.debug(data)
    try:
        response = post(url, data=str(data))
    except (ConnectionError, ChunkedEncodingError, ReadTimeout):
        logging.error('Can\'t connect to Artemis to set color')
        return
    if response.status_code != 200:
        logging.debug(response.content)
        logging.warning(f'Status code is not 200. Data: {data}')
