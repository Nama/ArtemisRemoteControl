from requests import get, post
from requests.exceptions import ConnectionError, ChunkedEncodingError, ReadTimeout
import logging
from os import environ
from json import loads

logging.basicConfig(filename='error.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)


def _getapiurl():
    txt_path = environ['ProgramData'] + '/Artemis/webserver.txt'
    url_endpoints = open(txt_path, 'r').readline() + 'plugins/endpoints'

    try:
        response = get(url_endpoints, timeout=0.3)
    except (ConnectionError, ChunkedEncodingError, ReadTimeout):
        logging.error('Can\'t connect to Artemis')
        return
    if response.status_code != 200:
        return
    endpoints = loads(response.content)
    url = ''
    for endpoint in endpoints:
        if endpoint['Name'] == 'AddOrReplace':
            url = endpoint['Url']
            break
    if url:
        return url
    else:
        logging.error('Couldn\'t get endpoint URL')
        return


def setleds(value: dict, url):
    if not url:
        url = _getapiurl()
    if not url:
        return
    logging.debug(value)
    try:
        response = post(url, json=value, timeout=0.3)
    except (ConnectionError, ChunkedEncodingError, ReadTimeout):
        logging.error('Can\'t connect to Artemis to send data')
        return
    if response.status_code != 200:
        logging.debug(response.content)
        logging.warning(f'Status code is not 200. Data: {value}')
    return url
