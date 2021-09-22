from requests import post
from requests.exceptions import ConnectionError, ChunkedEncodingError, ReadTimeout
import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)


def setleds(name: str, value: dict):
    url = 'http://localhost:9696/json-datamodel/'
    logging.debug(value)
    try:
        response = post(f'{url}{name}', json=value, timeout=0.3)
    except (ConnectionError, ChunkedEncodingError, ReadTimeout):
        logging.info('Can\'t connect to Artemis to send data')
        return
    if response.status_code != 200:
        logging.debug(response.content)
        logging.error(f'Status code is not 200. Data: {value}')
