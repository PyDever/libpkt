
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
import libpkt
import socket
import random

# build your own packet
pkt = libpkt.IP(src_ip=socket.gethostbyname(socket.gethostname()), 
                dst_ip=socket.gethostbyname(socket.gethostname())
                ip_id=1503327, d_hdr=random._urandom(1024))
print pkt.bin
```
```shell
���<ք��{�g��b3y���H\��w�yK�d�V;�L��.�uZ�/��}�5x�@�0�]�[��m�S��E�}��2>�lS��1�b\>��Wօ��8E��z~$����J�b
�"R�[�)$��[�=�%�c�\�jP�\��Z�'��Z*�$p{���N��H�S@��ߩ���nj@�(���!Hr4v0���� @���6���}���̗x��E
                       q�@Z�

��nZ���^�Ւ��8e��������F���M谟`M邉�d
                                        wI�v���jί�'`5����)kb����Q�QohK;�A��1����������A
                ���u�i�y5
Dh��rF�jBX�[_T�1h�|���o��_�K	t=8@|�M�Z21c?w �ˆ1���7�������V�"q�/�!H6�I�򵩖�}���'܍P%�L����.�{,��\Χ���g+����5��()���vR����I��Y��.1Sm�Aw���SO���Sb�/�d
 f�"o�)q C�˒�o�EC�]n�R��Θֹ�	�~�h>LS��EUr��w͓�_�OV��	T#Ȇ�)u;�f%V����J��i���5,��ᤜ/e��f���H;�o��Uy�Jn�����QT�,�@��u�:
                                                        �X�R��8\�F"Z6��r2����w>�����O\j�G�B0Z�^��$�oa�g��aUA�e��Ȑ��Ϙ�sniT<k��Lq���5)��ͻ��[
=S�w�f:�-^ҷ�!��ɚ��9H
                    ��=R�
l���p*0�����5 ��!N^!fD���M�J���;����/�z��T�����2�U���*qA`TF?���3d�+Ҍ��v/_�v2�
  ,+�x����&��]^��s2������9��U�*Y"�m�B'V{�S��ل�\i��Yrs*��'=H
                                                              ��
                                                                �����Y��Z�
```

  * ***fast*** packet capture algorithm
  * ***fast*** packing and unpacking
  * efficient data injection
  * ***faster*** THAN SCAPY!


