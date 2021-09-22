#!/usr/bin/env python

from asyncio import run, sleep
from threading import Thread
from subprocess import check_output
from artemisremotecontrol import setleds


async def loop():
    while True:
        output = check_output('powercfg /GetActiveScheme')
        activeplan = output.decode('utf-8').split('(')[1][:-1]
        await setleds('PowerPlan', {'powerplan': activeplan})
        await sleep(3)


tloop = Thread(target=lambda: run(loop()))
tloop.start()
