
<img src="https://thumbs.dreamstime.com/b/oriental-pitcher-vector-drawing-ancient-jug-east-style-30405033.jpg" width="150"><img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="320"/>

 [![Build status](https://ci.appveyor.com/api/projects/status/pjxh5g91jpbh7t84?svg=true)](https://ci.appveyor.com/project/tygerbytes/resourcefitness) 
[![Coveralls](https://coveralls.io/repos/github/tygerbytes/ResourceFitness/badge.svg?branch=master)](https://coveralls.io/github/tygerbytes/ResourceFitness?branch=master) 
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
<br>
# libpkt

libpkt is a simple packet manipulation library for Python. It is specially designed to
efficiently handle TCP/IP packets. 

```
$ make build
```

NOTE: libpkt only runs on UNIX systems!

```python
>>> import libpkt
>>> import socket
>>> import random

>>> # build your own packet
>>> pkt = libpkt.IP(src_ip=socket.gethostbyname(socket.gethostname()), 
                dst_ip=socket.gethostbyname(socket.gethostname())
                ip_id=1503327, d_hdr=random._urandom(1024))
>>> pkt.d_hdr
�������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g�

>>> pkt.src_ip
'127.0.1.1'

>>> pkt.dst_ip 
'127.0.1.1'

>>> # print the entire packed packet
>>> pkt.bin
�������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g��������G�2����������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g�
```
The `libpkt.IP.bin` object is actually an `@property` method. This object is what you 
use to send a TCP/IP packet in raw form.

```python
>>> psock = libpkt.PSocket(timeout=10)
>>> psock.sendp(pkt.bin, dst_ip=pkt.dst_ip, dst_p=80)
True
```
Capturing packets is just as easy using `libpkt.PSocket.recvp`.

```python
>>> # listen for one TCP/IP packet on the line
>>> pkt2 = psock.recvp(live=True, max_bb=65565, count=1)[0]
'E\x00\x00<\x11\x8a\x00\x00<\x062\x07\xac\xd9\x05N\xc0\xa8\xc8[\x00P\xacL\xdb\x92\xca0\xcd\x86R\x14\xa0\x12\xeb b\x9e\x00\x00\x02\x04\x05d\x04\x02\x08\n\xa20\xf5\x07|\x969\x8a\x01\x03\x03\x08'
```

The `pkt2` object or in other words whatever `psock.recvp` returns is not as fancy
as `libpkt.IP`. You cannot just say `pkt2.d_hdr` to get the data or `pkt2.src_ip` to
get the source address. There is however a built-in `libpkt` method to
parse these captured packets.

```python
>>> libpkt.read(pkt2)
```


  * ***fast*** packet capture algorithm
  * ***fast*** packing and unpacking
  * efficient data injection
  * ***faster*** THAN SCAPY!


