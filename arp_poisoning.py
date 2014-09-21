#!/usr/bin/env python


import os
import sys
import argh


def _assure_root(fn):
    def wrapper(*args, **kwargs):
        if not os.geteuid() == 0:
            sys.exit("\nOnly root can run this script\n")
        return fn(*args, **kwargs)
    return wrapper


@_assure_root
def poison():
    pass


@_assure_root
def verify():
    pass


@_assure_root
def monitor():
    pass


@_assure_root
def display():
    pass


if __name__ == '__main__':
    argh.dispatch_commands([poison,
                            verify,
                            monitor,
                            display])
