pysect
======

_Security related scripts and tools, implemented for fun_

This projects aims to help me have fun, creating a demand for myself practing and refreshing some networking concepts. For now - and probably for a long time - it will not be handled as a serios project: do not expect continuation.


### Summary

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

