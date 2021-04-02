import logging
from shutil import move
from json import dump, load, JSONDecodeError


class Config:
    def __init__(self):
        self.path = 'config.json'
        self.config = None

    def load(self, script):
        try:
            with open(self.path, 'r') as configfile:
                self.config = load(configfile)
                logging.debug('Config loaded')
                configfile.close()
                return self.config
        except FileNotFoundError:
            logging.debug('No config found. Creating new one.')
        except JSONDecodeError:
            logging.warning('Corrupted config. Creating new one.')
            move(self.path, self.path + 'corrupt.json')
        self.config = None
        self.init(script)

    def save(self):
        with open(self.path, 'w') as configfile:
            dump(self.config, configfile, sort_keys=True, indent=4)
            logging.debug('Config saved.')
            configfile.close()

    def init(self, script):
        # Creating new config file
        logging.debug('Creating new config')
        self.config = {script: []}
        self.save()

    def add(self, script, data):
        self.config[script].append(data)
        self.save()
