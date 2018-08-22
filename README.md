 [![Build status](https://ci.appveyor.com/api/projects/status/pjxh5g91jpbh7t84?svg=true)](https://ci.appveyor.com/project/tygerbytes/resourcefitness) 
[![Coveralls](https://coveralls.io/repos/github/tygerbytes/ResourceFitness/badge.svg?branch=master)](https://coveralls.io/github/tygerbytes/ResourceFitness?branch=master) 

## Installing libpkt
libpkt can be installed using Make. 
```
$ make build
```
NOTE: libpkt only runs on UNIX systems!

```python
from libpkt import pkt

new_packet = pkt.make(
    src_ip='127.0.0.1', 
    dst_ip='198.148.81.136', 
    ip_id=54321, ip_ver=4, tcp_seq=454,
    d_hdr=random._urandom(1024)
)
```

## About libpkt
libpkt is a simple packet manipulation library for Python. It is specially designed to
efficiently handle TCP/IP packets. 

  * ***fast*** packet capture algorithm
  * ***fast*** packing and unpacking
  * efficient data injection
  * ***faster*** THAN SCAPY!


