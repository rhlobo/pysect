#!/usr/bin/env python


import argh


def poison():
    pass


def verify():
    pass


def monitor():
    pass


def display():
    pass


if __name__ == '__main__':
    argh.dispatch_commands([poison,
                            verify,
                            monitor,
                            display])
