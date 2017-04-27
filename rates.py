#!/usr/bin/env python

import re
import sys
import time
import curses
import signal
import profile
import commands
import operator
# import subprocess

def core(package):
    rx = sum(package[ 1: 7])
    tx = sum(package[ 9:15])
    byte = package[0] + package[8]
    return {'package' : rx + tx}

def extract(interface):
    # try:
        command = 'cat /proc/net/dev | grep ' + interface
        output = commands.getoutput(command)
        # commands is faster than subprocess, however, it is not supported in py3
        # output = subprocess.check_output(command, shell=True).strip()
        timestamp = time.time()
        # re-format output
        statistic = re.compile("[ ]+").split(output)
        while '' in statistic:
            statistic.remove('')
        # compute package amount
        data = core(map(int, statistic[1:]))
        return {
            'data'      : [data['package'], timestamp],
            # 'output'    : output
            }
    # except subprocess.CalledProcessError as e:
        # output = e.output
        # code   = e.returncode


def difference(previous, interface):
    current = extract(interface)
    delta = map(operator.sub, current['data'], previous['data'])
    # print(prv)
    # print(cur)
    return {
        'delta'     : delta,
        'current'   : current
        }


def signal_handler(signal, frame):
    sys.exit(0)


def monitor(window, interface):
    window.addstr( 8,  3, "Monitoring " + interface + "...")
    
    previous = extract(interface)
    # for i in range(0, 1000):         # performance_wrapper
    while True:
        ret = difference(previous, interface)
        previous = ret['current']
        window.addstr(10, 3, "dP/dT: " + str(ret['delta'][0] / ret['delta'][1]) + " pkg/s")
        # window.addstr(12, 7, "dP: " + str(ret['delta'][0]) + " pkg(s)")
        window.addstr(13, 7, "dT: " + str(ret['delta'][1]) + " ms")
        # window.addstr(14, 7, "real: " + str(time.time()))
        # window.addstr(17, 1, ret['current']['output'])
        window.refresh()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    interface = raw_input("interface: ")
    curses.wrapper(monitor, interface)
    # profile.run("curses.wrapper(monitor, 'eth0')")
