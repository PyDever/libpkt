## Installation
libpkt can be installed using Make. 
```
$ make build
```
NOTE: libpkt only runs on UNIX systems!

## About libpkt
libpkt is a simple packet manipulation library for Python. It is specially designed to
efficiently handle TCP/IP packets. 

  * ***fast*** packet capture algorithm
  * ***fast*** packing and unpacking
  * efficient data injection
  * ***faster*** THAN SCAPY!
  
 libpkt ***only*** has ***standard library*** dependencies!
 
  * `socket` for obvious reasons
  * `struct` for C-esk functionality
  * `random` for byte generation
  * `time` for plotting delays
  * `array` for low-level structures
  * `fcntl` for low-level file control

## Contributions
Contributions are welcome, however please read the [guidlines](google.com).

## Small API Documentation

libpkt has smaller sub-modules that do specific things. 

 * `ifs` for low-level newtwork interface control
 * `pkt` for packet manipulation
 * `psocket` for sniffing and sending packets

### ifs module 

Let us learn the `ifs` module first. As you may know, every computer
has a network card that houses multiple interface. The interface's IP address is 
your IP address! Let us grab a list of interfaces!
```python
from libpkt import ifs

# grab a list of interfaces
print ifs.l()
```
*output*
```python
[('lo', '\x7f\x00\x00\x01'), ('enp0', '\xc0\xa8\xc8[')]
```
As you can see, we have two main interfaces: `lo` and `enp0`. To the right of that interface
is the address... its heavily encoded. Let us format our IP using `fmt_ip`.
```python
from libpkt import ifs

# grab the lo interface
lo = ifs.l()[0]

# get the IP attached to an intrerface
print ifs.fmt_ip(lo)
```
*output*
```python
127.0.0.1
```
As you might have expected, I have a typical interface IP.  You can get all interface IPs 
using `fmt_summary`. This way is more efficient and actually faster.

```python
from libpkt import ifs

# grab all interfaces
interfaces = ifs.l()

# get address of all interfaces
print ifs.fmt_summary(interfaces)
```



