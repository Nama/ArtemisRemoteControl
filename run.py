#!/usr/bin/env python

from os import mkdir
from os.path import isdir
from simple_plugin_loader import Loader

# initialize the loader
loader = Loader()

if not isdir('scripts'):
    mkdir('scripts')

# load your plugins
plugins = loader.load_plugins('scripts')
