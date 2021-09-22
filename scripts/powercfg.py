#!/usr/bin/env python

from time import sleep
from threading import Thread
from subprocess import check_output
from artemisremotecontrol import setleds


def loop():
    while True:
        output = check_output('powercfg /GetActiveScheme')
        activeplan = output.decode('utf-8').split('(')[1][:-1]
        setleds('PowerPlan', {'powerplan': activeplan})
        sleep(3)


tloop = Thread(target=loop)
tloop.start()
