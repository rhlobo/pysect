pysect
======

_Security related scripts and tools, implemented for fun_

This projects aims to help me have fun, creating a demand for myself to practice and refresh some networking concepts. For now - and probably for a long time - it will not be handled as a serios project: do not expect periodic updates...


### Summary

#### MAC Discovery and Disconnection

Sniffs packets and prints out every distinct MAC Addresses found. Provides an option to disconnect each client found from the network (de-auth).

Usage:
````bash
$ sudo ./wifi_discover_macs.py -h
usage: wifi_discover_macs.py [-h] {discover,disconnect} ...

positional arguments:
  {discover,disconnect}
    discover
    disconnect

optional arguments:
  -h, --help            show this help message and exit
````

Examples:
````bash
$ sudo ./wifi_discover_macs.py discover
````

#### MAC Flooding

MAC flooding is a technique employed to compromise the security of network switches, possibly enabling the uso of tools such as ARP spoofing and packet analyzers. The outcome of this attack may vary across implementations, however the desired effect is to force legitimate MAC addresses out of the MAC address table, causing significant quantities of incoming frames to be flooded out on all ports.

#### Proxy

The `primitive_proxy.py` script is a simple flask server that uses the full _url_ for each request it receives to make a request to the real server. It wait for the answer, later on returning it to whoever made the request for it.

__In order to make it work, you need to spoof the desired DNS on the "requestant" machine.__ Manual test it by altering the `/etc/hosts` file.


### Backlog - Ideas

- Create APR poisoning tool
- Implement sslstrip features
- Integrate with mitm-proxy
    - Record traffic
    - Change traffic
    - Monitor traffic
        - Save passwords for known services
        - Save cookie / header information
- Highjack sessions
- Create DNS spoofing tool
- Create fake web app servers
    - Save logged passwords
    - Save cookie / header information

__IMPORTANT__: I cannot assure what (and when) I will end implemented.


### Contribution

Feel free to fork;
Pull requests are welcomed;

