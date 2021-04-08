#!/usr/bin/env python
import sys
import argparse
from pathlib import Path
from simple_plugin_loader import Loader


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='increase output verbosity of plugin loader',
                        action='store_true')
    parser.add_argument('-p', '--path', help='specify an alternative plugin path '
                                             '(relative, will be created if it doesn\'t exists)', default='scripts')
    args = parser.parse_args()

    # initialize the loader
    loader = Loader()
    scripts_path = Path(args.path)
    scripts_path.mkdir(exist_ok=True)

    if sys.platform != 'win32':
        print('ArtemisRemoteControl can only run on Windows')
        sys.exit(1)

    # load your plugins
    return loader.load_plugins(args.path, verbose=args.verbose)
