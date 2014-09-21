#!/usr/bin/env python


import os
import sys


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


def ip_forwarding():
    return Syscfg('/proc/sys/net/ipv4/ip_forward', '1\n')
