#!/usr/bin/env python


import os
import sys
import signal


def config_graceful_exit():
    def signal_handler(signal, frame):
        print 'Exiting...'
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


def assure_root():
    if not os.geteuid() == 0:
        sys.exit("\nAborting! This tool needs super user permissions.\n")


def _assure_root(fn):
    def wrapper(*args, **kwargs):
        assure_root()
        return fn(*args, **kwargs)
    return wrapper


class Syscfg(object):

    def __init__(self, filepath, value):
        self._filepath = filepath
        self._new_value = value

    @_assure_root
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
