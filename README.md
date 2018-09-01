
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
�������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g��������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g�
�������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g�
�������G�2���;�/ꖛK]�Hhu��y���jo��*�����31%ő��.���8F�Aq5�y����kXUUtG�SҠ��«T�Ġk�lɆ��M��D%�qBn��_˝P�{?�L��r-x��X����,@�+��^>|;ЍA�vJ+g� 
```



  * ***fast*** packet capture algorithm
  * ***fast*** packing and unpacking
  * efficient data injection
  * ***faster*** THAN SCAPY!


