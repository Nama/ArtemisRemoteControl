#!/usr/bin/env python

from time import sleep
from threading import Thread
from subprocess import check_output
from artemisremotecontrol import setleds

endpoint_url = None


def loop():
    global endpoint_url
    while True:
        output = check_output('powercfg /GetActiveScheme')
        activeplan = output.decode('utf-8').split('(')[1][:-1]
        endpoint_url = setleds({'PowerPlan': {'powerplan': activeplan}}, endpoint_url)
        sleep(3)


tloop = Thread(target=loop)
tloop.start()
